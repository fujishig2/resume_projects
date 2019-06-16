document.getElementById("date").innerHTML = Date();

window.alert("hello!");
console.log("hehe!");
document.write("123~");
window.alert(typeof "");
window.alert(typeof "");

document.getElementById("date").style.fontSize = "25px";
document.getElementById("date").style.color = "red";
document.getElementById("date").style.backgroundColor = "yellow"

function f1() {
   document.getElementById("lol").innerHTML = "hello world!";
   document.getElementById("date").innerHTML = Date();
}

function f2() {
   var j = 0;
   for (var i = 0; i < 10; i++) {
       j += i;
   }
   document.getElementById("counting").innerHTML = j;
   document.getElementById("bool").innerHTML = i == j;
}

var person = {
  firstName: "John",
  lastName : "Doe",
  id       : 5566,
  fullName : function() {
    return this.firstName + " " + this.lastName;
  }
};
document.getElementById("person").innerHTML = person.fullName() + " id: " + person.id;
