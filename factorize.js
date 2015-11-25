//This value is not provided when the function is called so, undefined has a value of a new instance of undefined
(function(undefined) {

//[start..end]
	function range(start, end) {
    	var total = [];

    	if (!end) {
        	end = start;
        	start = 0;
    	}

    	for (var i = start; i < end; i += 1) {
        	total.push(i);
    	}

    	return total;
	}		

//Primes cannot be factorized further and then for each factor in the composite number, factorize it and put it in the result
	var factorize = function(x) {
		if(isPrime(x))
			return x;
		else 
			var result = [];
			getMiddle(factors(x)).forEach(function(i){
				result.push(factorize(i));
			});
			return result;
	}

//If x % n == 0 then n is a factor of x. range(2,x-1) skips 1 and x
	var factors = function(x) {
		var result = [];
		range(2,x-1).forEach(function(i){
			if(x % i == 0)
				result.push(i);
		});
		return result;
	}

//Primes always have two factors, but we're skipping 1 and n so 0
	var isPrime = function(x) {
		return factors(x).length == 0;
	}

//Return a pair of numbers that multiply to give original.
	var getMiddle = function(x) { 
	return [x[0],x[x.length-1]];
	}
	
	var main = function() {
		console.log(factorize(16006));
	}

	main();
})();