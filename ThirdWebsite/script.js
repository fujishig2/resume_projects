function fibonacci(N){
	N = eval(N);
	if (N < 1) {
		document.getElementById("fib").innerHTML = 0;
		return;
	} else if (N < 2) {
		document.getElementById("fib").innerHTML = 1;
		return;
	}
	var f, s;
	f = 0; s = 1;
	for (var i = 1; i < N; i++) {
		[f, s] = [s, f+s];
	}
	document.getElementById("fib").innerHTML = s;
}

function countdown(N) {
	if (N < 0) return;
	setTimeout(function() {
			countdown(N-1);
		}, 1000);
	document.getElementById("count").innerHTML = N;
	if (N <= 0) {
		window.alert("Finished!");
	}
}

function openPage(str) {
	//window.open(str + ".html");
	parent.location= str + ".html";
}

function buttonPress(val) {
	document.getElementById("calcInput").value = document.getElementById("calcInput").value + val;
}

function buttonClear() {
	document.getElementById("calcInput").value = "";
}

function buttonBack() {
	var str = document.getElementById("calcInput").value;
	document.getElementById("calcInput").value = str.substring(0, str.length - 1); 
}

function buttonSubmit() {
	try {
		document.getElementById("calcInput").value = eval(document.getElementById("calcInput").value);
	} catch (err) {
	document.getElementById("calcInput").value = "Undefined";
	}
}

function mergeSort(str) {
	var arr = str.split(',');
	for (var i = 0; i < arr.length; i++) {
		arr[i] = arr[i].replace(/^\s+|\s+$/g, '');
	}
	var merg = mergeSortHelper(arr);
	document.getElementById("sortinput").value = merg.toString();
}

function mergeSortHelper(arr) {
	var merge = [];
	if (arr.length > 1) {
		var mid = Math.floor(arr.length/2);
		var merg1 = mergeSortHelper(arr.slice(0, mid));
		var merg2 = mergeSortHelper(arr.slice(mid, arr.length));
	} else {
		return arr;
	}
	var i = 0, j = 0;
	while (i < merg1.length || j < merg2.length) {
		if (parseInt(merg1[i]) <= parseInt(merg2[j])) {
			merge.push(merg1[i]);
			i++;
		} else if (parseInt(merg2[j]) < parseInt(merg1[i])) {
			merge.push(merg2[j]);
			j++;
		} else if (i >= merg1.length) {
			merge.push(merg2[j]);
			j++;
		} else if (j >= merg2.length) {
			merge.push(merg1[i]);
			i++;
		}
	}
	return merge;
}
	
