// Natural Neighbor Interpolation following the CGAL User Manual:
// https://doc.cgal.org/latest/Interpolation/index.html

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <omp.h>

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Delaunay_triangulation_2.h>
#include <CGAL/natural_neighbor_coordinates_2.h>
#include <CGAL/interpolation_functions.h>


typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef K::FT                                         Coord_type;
typedef K::Point_2                                    Point;
typedef CGAL::Delaunay_triangulation_2<K>             Delaunay_triangulation;
typedef std::vector< std::pair<Point, Coord_type> >   Coordinate_vector;
typedef std::map<Point, Coord_type, K::Less_xy_2>     Point_value_map;
typedef std::vector<int>                              Vint;
typedef std::vector<double>                           Vdouble;
typedef std::vector<std::vector<double>>              Vdouble2d;


// https://stackoverflow.com/questions/32102340/how-can-a-create-a-define-to-create-a-2d-vector
template<typename T>
std::vector<std::vector<T>> make_2d_vector(std::size_t rows, std::size_t cols)
{
    return std::vector<std::vector<T>>(rows, std::vector<T>(cols));
}


Vdouble2d nninterpol(Vint x, Vint y, Vdouble z, int ncols, int nrows) {

    int ntrainpoints = size(x);
    Vdouble2d raster = make_2d_vector<double>(nrows, ncols);

    std::vector<Point> points;
    points.reserve(ntrainpoints);

    Delaunay_triangulation T;
    Point_value_map values;

    for(int i=0; i<ntrainpoints ; i++){
        Point p(x[i], y[i]);
        points.push_back(p);
        values.insert(std::make_pair(p, z[i]));
    }

    T.insert(points.begin(), points.end());

    // Optimization (Face_handle look-up + OpenMP) following:
    // https://stackoverflow.com/questions/30354284/cgal-natural-neighbor-interpolation
    Delaunay_triangulation::Face_handle fh;

    #pragma omp parallel for private(fh)
    for(int row=0; row<nrows; row++) {
        for(int col=0; col<ncols; col++) {
            Point p(col, row);
            fh = T.locate(p, fh);
            std::vector< std::pair< Point, Coord_type > > coords;
            CGAL::Triple<std::back_insert_iterator<Coordinate_vector>, K::FT, bool> natneighbor = CGAL::natural_neighbor_coordinates_2(T, p, std::back_inserter(coords), fh);

            // error checking following:
            // https://github.com/remotesensinginfo/spdlib/blob/cf88633bd068638b13fb7701d93f01a28a8cd488/src/spd/SPDPointInterpolation.cpp
            if(!natneighbor.third)
            {
                raster[row][col] = std::numeric_limits<float>::signaling_NaN();
            }
            else
            {
                raster[row][col] = CGAL::linear_interpolation(coords.begin(), coords.end(), natneighbor.second, CGAL::Data_access<Point_value_map>(values));
            }
        }
    }

    return raster;
}

PYBIND11_MODULE(nninterpol, m) {
    m.doc() = "Natural Neighbor Interpolation using CGAL";
    m.def("nninterpol", &nninterpol, "Natural Neighbor Interpolation using CGAL");
}
