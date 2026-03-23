#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "spatialindex" for configuration "Release"
set_property(TARGET spatialindex APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(spatialindex PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libspatialindex.so.8.0.0"
  IMPORTED_SONAME_RELEASE "libspatialindex.so.8"
  )

list(APPEND _cmake_import_check_targets spatialindex )
list(APPEND _cmake_import_check_files_for_spatialindex "${_IMPORT_PREFIX}/lib/libspatialindex.so.8.0.0" )

# Import target "spatialindex_c" for configuration "Release"
set_property(TARGET spatialindex_c APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(spatialindex_c PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libspatialindex_c.so.8.0.0"
  IMPORTED_SONAME_RELEASE "libspatialindex_c.so.8"
  )

list(APPEND _cmake_import_check_targets spatialindex_c )
list(APPEND _cmake_import_check_files_for_spatialindex_c "${_IMPORT_PREFIX}/lib/libspatialindex_c.so.8.0.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
