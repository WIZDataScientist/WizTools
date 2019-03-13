#' Get Dropbox Path Function
#'
#' This function allows you to obtain the path for your local dropbox folder.
#' @param business Business Dropbox or Personal Dropbox? Defaults to FALSE.
#' @keywords dropbox
#' @export
#' @examples
#' GetDropboxPath()

GetDropboxPath <- function(business = F){
  if(!require("jsonlite")) install.packages("jsonlite",dependencies = TRUE);library("jsonlite")
  if(!require("dplyr"))    install.packages("dplyr",dependencies = TRUE);   library("dplyr")

  file_name <- list.files(paste(Sys.getenv(x = "APPDATA"),"Dropbox", sep="/"), pattern = "*.json", full.names = T)

  if (length(file_name) == 0)
    file_name <- list.files(paste(Sys.getenv(x = "LOCALAPPDATA"),"Dropbox", sep="/"), pattern = "*.json", full.names = T)

  if(business == T)
    return(fromJSON(txt = file_name)$business$path)
  else
    return(fromJSON(txt = file_name)$personal$path)

}
