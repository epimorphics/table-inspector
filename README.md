# table-inspector

Python csv analysis tool.

## Tools

key_columns: produces the key column, of combination of columns that make a key column, for given csv file(s). If there are multiple candidate key columns, all are given as output.

controlled_terms: columns that have far less distince values than the number of rows suggest coded values, so controlled_terms finds candidates columns that use similar values allowing for a quick check. Does this up to maximum size combination of columns, across multiple files.

denormalised_concepts: finding columns whose values co-occur with each other. Does this up to maximum size combination of columns, across multiple files.
Does this up to maximum size combination of columns.

## Testing

Testing is done using the 'unittest' library.

## Running Programs

All programs can be run on a single file or a directory of files, using either the '-f' (for singel file) or '-d' (for directory) arguments, followed by the file or directory.
