/**
 * Created by yang on 16-10-7.
 */
function setTableBC() {
    $("#select_table tbody tr:odd").css("background-color","#f6f4f0");
    $("#select_table tbody tr:even").css("background-color","#fff");
}
function dropCourse($target) {
    $.ajax({
        type:"POST",
        url:"/SCS/student_drop_course/",
        data:{
            "course_id":$target.closest("tr").attr("data-id"),
        },
        success:function (data,textStatus) {
            var theJson=eval("("+data+")");
            if(theJson["res"]==="success"){
                $.myAlert("退选成功");
                var $tbody=$target.closest("tbody");
                $target.closest("tr").remove();
                if(!$tbody.children().length) {
                    $tbody.append("<tr><td colspan='7' class='table_btn_td'><div id='no_course_tip'>没有已选课程</div></td></tr>");
                }
                setTableBC();
            }else {
                $.myAlert("退选失败");
            }
        }
    })
}
function selectTable(event) {
    var $target=$(event.target);
    if($target.hasClass("look_lt_btn")){
        deallookLT(event,$target);
    }else if($target.hasClass("drop_btn")){
        $.myConfirm({
            message:"是否退选此课程？",
            trueCallback:function(){dropCourse($target)},
        });
    }
}
$(document).ready(function () {
    $("#left_arrow").detach().appendTo($("#left ul li:eq(2)"));
    setTableBC();
    $("#select_table tbody").click(selectTable);
});

