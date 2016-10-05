/**
 * Created by yang on 16-10-3.
 */

function loginBackgroundRoll() {
    var $currentBackground=$("#login_background img.current"),
        $next;
    if($currentBackground.is("#login_background img:last")){
        $next=$currentBackground.siblings().eq(0);
    }else{
        $next=$currentBackground.next();
    }
    $currentBackground.removeClass("current").stop().fadeOut(800);
    $next.addClass("current").stop().fadeIn(800);
}

$(document).ready(function () {
    $("#login_background img.current").show();
    var loginBackgroundRollId=setInterval(loginBackgroundRoll,5000);
    //$("div.login").addClass("login_show");
    $("#login").fadeIn(1000);
});