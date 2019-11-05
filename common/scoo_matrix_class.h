//
// Created by egi on 11/5/19.
//

#ifndef MATRIX_FORMAT_PERFORMANCE_SCOO_MATRIX_CLASS_H
#define MATRIX_FORMAT_PERFORMANCE_SCOO_MATRIX_CLASS_H

#include <matrix_market_reader.h>
#include <memory>

template <typename data_type>
class csr_matrix_class;

/// Sliced COO Format
template <typename data_type>
class scoo_matrix_class
{
public:
  scoo_matrix_class () = delete;
  explicit scoo_matrix_class (csr_matrix_class<data_type> &matrix);

  const matrix_market::matrix_class::matrix_meta meta;

public:
  std::unique_ptr<data_type[]> values;
  std::unique_ptr<unsigned int[]> c_index;
  std::unique_ptr<unsigned int[]> r_index;
  std::unique_ptr<unsigned int[]> index;

private:
  size_t elements_count {};
};


#endif // MATRIX_FORMAT_PERFORMANCE_SCOO_MATRIX_CLASS_H
