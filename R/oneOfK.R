OneOfK <- function(data, maxLabels = 10){
  
  # ----------------------------------------------------------
  # If we have character variables make it to factor variables
  # ----------------------------------------------------------
  varChar <- colnames(data)[sapply(data, is.character)]
  
  for(name in varChar){
    data[,name] <- as.factor(data[,name])
  }
  
  # ----------------------------------------------------------
  # Create a list if categories or levels in a factor
  # ----------------------------------------------------------
  cat      <- colnames(data)[sapply(data, is.factor)]
  cat      <- lapply(data[,cat], levels)
  # if(any(duplicated(unlist(cat))))
  #   cat      <- lapply(data[,cat], function(x) paste0(cat,'_',levels))
  
  # Number of labels:
  N_labels <- lapply(cat, length)
  
  # ----------------------------------------------------------
  # Does any variables have too many labels compared to maxLabels ?
  # If yes then stop and return an error
  # ----------------------------------------------------------
  varTooBig <- sapply(seq_len(length(N_labels)), function(x) N_labels[[x]] > maxLabels) #logical class: var has too many labels?
  if(any(varTooBig)){
    stop(paste0(names(N_labels)[varTooBig]), " has too many labels. It has ", N_labels[varTooBig], " labels and maximum allowed is ", maxLabels, ".")
    break();
  }
  
  # ----------------------------------------------------------
  # Creating M1, a dataset without any factor variables
  # ----------------------------------------------------------
  M1 <- data[, !colnames(data) %in% names(cat)]
  # ----------------------------------------------------------
  # Creating M2, a data frame with the 1-out-of-k-coded data
  # ----------------------------------------------------------
  M2 <- list()
  
  # For each factor with c number of levels
  for(i in seq_len(length(cat))){
    
    # create a dataframe with dimension n times c 
    # where each c variables are 1 or 0 indicating if the observation belong to level c
    tmp           <- lapply(seq_along(cat[[i]]), function(x) ifelse(data[,names(cat)[i]] == cat[[i]][x], 1L, 0L))
    tmp           <- data.frame(tmp)
    colnames(tmp) <- cat[[i]]
    
    # assign to a list
    M2[[i]] <- tmp
    
    rm(tmp)
  }
  
  # cbind all the dataframes on M2
  M2 <- do.call(cbind, M2)
  
  # ----------------------------------------------------------
  # cbind both M1 and M2 to get return the final data
  # ----------------------------------------------------------
  M <- cbind(M1, M2)
  
  cat(ifelse(all(rowSums(M2) == length(cat)), "All OK!", "rowSums is not equal to number of factors"))
  Sys.sleep(1)
  
  return(M)
  
}