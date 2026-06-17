import pyarrow.parquet as pq


def get_schema(file_path):
    pf = pq.ParquetFile(file_path)

    schema = []
    arrow_schema = pf.schema_arrow

    # Read first row group only for sampling
    sample_table = None
    if pf.num_row_groups > 0:
        sample_table = pf.read_row_group(0)

    for i, field in enumerate(arrow_schema):
        col_name = field.name
        dtype = str(field.type)

        # ✅ Null count (accurate across row groups)
        null_count = 0
        for rg in range(pf.num_row_groups):
            column_chunk = pf.metadata.row_group(rg).column(i)
            stats = column_chunk.statistics

            if stats is not None and stats.null_count is not None:
                null_count += stats.null_count

        # ✅ Sample value from first row group
        sample_value = None
        if sample_table and col_name in sample_table.column_names:
            col_array = sample_table[col_name].to_pylist()
            for val in col_array:
                if val is not None:
                    sample_value = val
                    break

        schema.append({
            "column": col_name,
            "dtype": dtype,
            "null_count": int(null_count),
            "sample_value": sample_value
        })

    return schema