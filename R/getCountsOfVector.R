#' Get Dropbox Path Function
#'
#' This function allows you to obtain the path for your local dropbox folder.
#' @param business Business Dropbox or Personal Dropbox? Defaults to FALSE.
#' @keywords dropbox
#' @export
#' @examples
#' GetDropboxPath()

getCountsOfVector <- function(Vector, setFirstColName = NULL) {
  
  DataFrame <- data.frame(table(Vector))
  
  if(is.null(setFirstColName))
    return(DataFrame)
  else
    return(setNames(DataFrame, nm = c(setFirstColName, "Freq")))
}