/**
 * Created by yang on 16-10-5.
 */
function headerDropdown(event) {
    event.stopPropagation();
    var $headerDropdown=$("#header_dropdown");
    $headerDropdown.slideToggle(200).click(function (event) {
        event.stopPropagation();
    });
    $("body,html").click(hideHeaderDropdown=function () {
        $headerDropdown.slideUp(200);
        $("body,html").unbind("click",hideHeaderDropdown)
    });
}

function signOut(event) {
    $.ajax({
        url:"/SCS/sign_out/",
        type:"POST",
        data:{},
        success:function (data,textStatus) {
            if(data==="success"){
                location.href="/SCS/"
            }
        }
    })
}
function caluWarpHeight(event) {
    var $warp=$("#warp");
    if($warp.outerHeight()+$("#header").height()<$(window).height()) {
        $warp.outerHeight($(window).height() - $("#header").height());
    }
}
function tableSelectPager(event) {
    window.location.href=$(this).attr("data-url")+$(this).children("option:selected").val()+"/";
}
function lookLT($target) {
    var course_id=$target.closest("tr").attr("data-id"),
        $ltDiv=$("<div class='course_location_time' data-id='"+course_id+"'><img class='loading_img' src='/static/image/system/loading.gif'><div class='course_dropdown_arrow_border'></div><div class='course_dropdown_arrow'></div></div>"),
        $ltTable=$("<table class='course_lt_table'><thead><tr><th>上课周次</th><th>上课节次</th><th>上课地点</th></tr></thead><tbody></tbody></table><div class='course_dropdown_arrow_border'></div><div class='course_dropdown_arrow'></div>");

    $.ajax({
        type:"POST",
        url:"/SCS/look_course_lt/",
        data:{
            course_id:course_id,
        },
        success:function (data,textStatus) {
            var jsonDict=eval("("+data+")");
            if(jsonDict["res"]==="success"){
                $ltDiv.find("img.loading_img").remove();
                var lts=jsonDict["lts"],
                    $ltTbody=$ltTable.find("tbody");
                for(var i=0;i<lts.length;i++){
                    $ltTbody.append("<tr><td>"+lts[i]["week"]+"</td>"+"<td>"+lts[i]["class"]+"</td>"+"<td>"+lts[i]["location"]+"</td></tr>");
                }
                $ltDiv.prepend($ltTable);
            }
        },
        beforeSend:function (XMLHttpRequest) {
            $ltDiv.css({top:$target.offset().top+$target.parent().height()+10,"left":$target.offset().left-225});
            $("body").append($ltDiv);
            $("html,body").click(function (event) {
                   $ltDiv.remove();
                    $("html,body").unbind("click",arguments.callee);
            });
        }
    })
}
function deallookLT(event,$target) {
    var $exist=$("div.course_location_time[data-id='"+$target.closest("tr").attr("data-id")+"']");
    if($exist.length){
        $exist.remove()
    }else{
        $("div.course_location_time").remove();
        event.stopPropagation();
        lookLT($target);
    }
}
$(document).ready(function () {
    caluWarpHeight();
    $(window).resize(caluWarpHeight);
    $("#header_dropdown_btn").click(headerDropdown);
    $("#sign_out").click(signOut);
    $("select.table_pager").change(tableSelectPager);
});
