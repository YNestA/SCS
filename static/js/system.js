/**
 * Created by yang on 16-10-5.
 */
function headerDropdown(event) {
    event.stopPropagation();
    var $headerDropdown=$("#header_dropdown");
    $headerDropdown.show().click(function (event) {
        event.stopPropagation();
    });
    $("body,html").click(hideHeaderDropdown=function () {
        $headerDropdown.hide();
        $("body,html").unbind("click",hideHeaderDropdown)
    });
}

function signOut(event) {
    $.ajax({
        url:"/SCS/sign-out/",
        type:"POST",
        data:{},
        success:function (data,textStatus) {
            if(data==="success"){
                location.href="/SCS/"
            }
        }
    })
}
$(document).ready(function () {
    $("#header_dropdown_btn").click(headerDropdown);
    $("#sign_out").click(signOut);
});
