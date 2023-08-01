#!/bin/bash


# ------ Names & URLs patterns

# Archive name pattern - format with $year
ZIP_PATTERN="OpenDataZNO%d.7z"
# Archive url pattern - format with $year
URL_PATTERN="https://zno.testportal.com.ua/yearstat/uploads/$ZIP_PATTERN"
# Data file name pattern - format with $year
CSV_PATTERN="Odata%dFile.csv"


# ------ Obtaining CMD arguments

echo_help() 
{
  self_name="$(basename "$0")"
  pad_len="$(("${#self_name}" + 8))"

  printf "Usage: %s %s\n"   "$self_name"              "[-Fd|--file-dir <arg>] [-y|--year <arg>]"
  printf "%*s%s\n"          "$pad_len" ""             "[-Bf|--ban-fails]"
  printf "%*s%s\n"          "$pad_len" ""             "[-Bf|--ban-fails]"
  printf "%*s%s\n"          "$pad_len" ""             "[-Cd|--cache-dir <arg>] [-Ck|--cache-keep]"
  printf "%*s%s\n"          "$pad_len" ""             "[-h|--help]"

  printf "\n%s\n\n"         "Options:"

  printf "  %-25s %s\n"     "-Fd, --file-dir <arg>"   "Data files directory - defaults to '.'"
  printf "  %-25s %s\n"     "-y, --year <arg>"        "Define years for which data files must be obtained."
  printf "\n"
  printf "  %-25s %s\n"     "-Bf, --ban-fails"        "Exit with error if one of tasks fails."
  printf "\n"
  printf "  %-25s %s\n"     "-Cd, --cache-dir <arg>"  "Directory for downloaded archives - defaults to file-dir"
  printf "  %-25s %s\n"     "-Ck, --cache-keep"       "Do not remove downloaded archives"
  printf "\n"
  printf "  %-25s %s\n"     "-h, --help"              "Show this help message and exit"
  printf "\n"
}


filedir="."       # Data files directory - defaults to '.'
years=()          # Passed years array

banfails=false    # Whether to exit with error if one of tasks fails.

cachedir=""       # Directory for downloaded archives - defaults to filedir
cacherm=true      # Whether to remove downloaded archives - defaults to true


# Iterate over arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in

    # Handle 'filedir' arg
    -Fd|--file-dir)
      filedir="$2"
      shift 2
      ;;
    
    # Handle 'cacherm' arg
    -Bf|--ban-fails)
      banfails=true
      shift
      ;;

    # Handle 'cachedir' arg
    -Cd|--cache-dir)
      cachedir="$2"
      shift 2
      ;;

    # Handle 'cacherm' arg
    -Ck|--cache-keep)
      cacherm=false
      shift
      ;;

    # Handle 'year' args
    -y|--year)
      years+=("$2")
      shift 2
      ;;

    # Handle 'help' flags
    -h|--help)
      echo_help
      exit 0
      ;;

    # Handle invalid options
    *)
      printf "Invalid option %s\n" "$1" >&2
      exit 1
      ;;

  esac
done

# Default 'cachedir' to 'filedir' if wasn't specified
if [ -z "$cachedir" ]; then cachedir="$filedir"; fi


# ------ Download data file for each year

# Function excutes existance checking 
# & downloading (if not exists) data file for passed year
handle_year()
{  
  local year="$1"

  csv_name="$(printf "$CSV_PATTERN" "$year")"   # Form data file name
  csv_path="$filedir/$csv_name"                 # Form data file path

  # Check if data file already exists
  if [ ! -f "$csv_path" ]; then

    printf "[%d] Data file not exists.\n" "$year"

    zip_path="$cachedir/$(printf "$ZIP_PATTERN" "$year")"   # Form archive file path

    # Check if archive file already exists
    if [ ! -f "$zip_path" ]; then
    
      printf "[%d] Downloading source archive...\n" "$year"
      curl "$(printf "$URL_PATTERN" "$year")" -o "$zip_path"; excode=$?   # Download archive by curl
      printf "\n"

      # Check was download successfull
      if [ $excode -ne 0 ]; then printf "[%d] Download failed. Skip.\n" "$year"; return 1; fi
      
      printf "[%d] Source archive downloaded.\n" "$year"
      
    else printf "[%s] Existing source archive found.\n" "$year"
    fi

    # Try to extract data file from archive
    printf "[%d] Extraxting data file from archive...\n" "$year"
    7z x "$zip_path" -ir!"$csv_name" -o"$filedir"; excode=$?
    printf "\n"

    # Check was extraction successfull
    if [ $excode -ne 0 ]; then printf "[%d] Extraction failed.\n" "$year"
    else printf "[%d] Data file extracted.\n" "$year"; fi

    # Remove source archive if needed
    if [ "$cacherm" = true ]; then rm "$zip_path"; printf "[%d] Archive file removed.\n" "$year"
    else printf "[%d] Archive file removing skipped.\n" "$year"; fi

    return $excode

  fi

  printf "[%d] Data file already exists.\n" "$year"
  return 0
}


# Iterate over passed years
for year in "${years[@]}"; do

  printf "[%d] HANDLING YEAR %d\n" "$year" "$year"

  # Run 'handle_year()' & check exit status
  if ! handle_year "$year"; then
    printf "[%d] Handling year %d failed.\n\n" "$year" "$year"
    if [ "$banfails" = true ]; then exit 1; fi
  else
    printf "[%d] Handling year %d finished successfuly.\n\n" "$year" "$year"
  fi

done
