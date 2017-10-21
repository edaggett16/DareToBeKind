function redirect_to_dare() {
	window.location.replace("/dare");
}

function redirect_to_main() {
	window.location.replace("/");
}

function redirect_to_user() {
	window.location.replace("/user");
}

function submit_alert(){
		if ($("#didDare").prop("checked")){
    	window.alert("You completed the dare! Your points have been recorded")
    	}
    	else{
    	window.alert("Go try out the dare and spread a little kindness!")}}
 
// function change_color1(){
// 	$("#home").css("background-color", "#C0C0C0")
// }
// function change_color2(){
// 	$("#aboutUs").css("background-color", "#C0C0C0")
// }
// function change_color3(){
// 	$("#myDares").css("background-color", "#C0C0C0")
// }
// function change_color4(){
// 	$("#memories").css("background-color", "#C0C0C0")
// }function change_color_back(){
// 	$(".top_button").css ("background-color", "#61a20c")
// }
function setup() {

    $("#kind").click(redirect_to_dare);
    $('#submissions').click(redirect_to_main);
  	$("#dareForm").submit(submit_alert);
    $("#user_dare").click(redirect_to_main);
 //    $("#home").mouseenter(change_color1);
	// $("#aboutUs").mouseenter(change_color2);
	// $("#myDares").mouseenter(change_color3);
	// $("#memories").mouseenter(change_color4);
	// $(".top_button").mouseleave(change_color_back);

}

$(document).ready(setup)