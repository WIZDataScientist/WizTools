#' Get Dropbox Path Function
#'
#' This function allows you to obtain the path for your local dropbox folder.
#' @param business Business Dropbox or Personal Dropbox? Defaults to FALSE.
#' @keywords dropbox
#' @export
#' @examples
#' GetDropboxPath()

orderBy <- function(DataFrame, by, decreasing = T) {
  
  if(!is.numeric(DataFrame[,by])){
    stop(paste(by, "must be numeric"));break
  }
  
  if(decreasing)
    return(DataFrame[order(-DataFrame[,by]), ])
  else 
    return(DataFrame[order(DataFrame[,by]), ])
}