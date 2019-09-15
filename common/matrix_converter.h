//
// Created by egi on 9/15/19.
//

#ifndef MATRIX_FORMAT_PERFORMANCE_MATRIX_CONVERTER_H
#define MATRIX_FORMAT_PERFORMANCE_MATRIX_CONVERTER_H

#include "matrix_market_reader.h"

#include <memory>

class csr_matrix_class
{
public:
  csr_matrix_class () = delete;
  explicit csr_matrix_class (matrix_market::matrix_class &matrix);

  const matrix_market::matrix_class::matrix_meta meta;

public:
  std::unique_ptr<double[]> data;
  std::unique_ptr<unsigned int[]> columns;
  std::unique_ptr<unsigned int[]> row_ptr;
};

#endif // MATRIX_FORMAT_PERFORMANCE_MATRIX_CONVERTER_H
