def roundwithzeroes(x):
	return str(round(x,2)) if (len(str(round(x,2)).split(".")[1]) == 2) else 	str(round(x,2))+"0" if len(str(round(x,2)).split(".")[0]) == 1 else 	str(round(x,2))+".00"