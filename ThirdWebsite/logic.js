function f1(N){
	if (N < 2) {
		document.getElementById("fib").innerHTML = N;
		document.getElementById("nextPage").style.display = "inline";
		return;
	}
	var f, s;
	f = 0; s = 1;
	for (var i = 1; i < N; i++) {
		[f, s] = [s, f+s];
	}
	document.getElementById("fib").innerHTML = s;
	document.getElementById("nextPage").style.display = "inline";
}

function f2(N) {
	if (N < 0) {
		return;
	}
	setTimeout(function() {
			f2(N-1);
			document.getElementById("nextPage").style.display = "inline";
		}, 1000);
	document.getElementById("count").innerHTML = N;
}
	
