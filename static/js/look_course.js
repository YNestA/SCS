function setTableBC() {
    $("#course_table tbody tr:odd").css("background-color","#f6f4f0");
    $("#course_table tbody tr:even").css("background-color","#fff");
}
function selectCourse($target) {
    $.ajax({
        type:"POST",
        url:"/SCS/student_select_course/",
        data:{
            "course_id":$target.closest("tr").attr("data-id"),
        },
        success:function (data,textStatus) {
            var theJson=eval("("+data+")"),
                $acTd=$target.closest("tr").children("td:eq(4)"),
                acDict= $acTd.text().split("/");
            if(theJson["res"]==="success"){
                $.myAlert("选修成功");
                acDict[0]=(parseInt(acDict[0])+1).toString();
                $acTd.text(acDict.join("/"));
            }else if(theJson["message"]==="full"){
                $.myAlert("人数已满");
                acDict[0]=acDict[1];
                $acTd.text(acDict.join("/"));
            }else if(theJson["message"]==="repeat"){
                $.myAlert("你已选修了此课程");
            }else if(theJson["message"]==="gt_two"){
                $.myAlert("你本学期已选修了两门课程");
            }
        },
    });
}
function dealCourseTable(event) {
    var $target=$(event.target);
    if($target.hasClass("prev_btn")||$target.hasClass("next_btn")){
        location.href=$target.attr("href");
    }else if($target.hasClass("look_lt_btn")){
        deallookLT(event,$target);
    }else if($target.hasClass("select_btn")){
        $.myConfirm({
            message:"是否选修此课程？",
            trueCallback:function(){
                selectCourse($target);
            },
        });
    }

}
$(document).ready(function () {
    $("#left_arrow").detach().appendTo($("#left ul li:eq(1)"));
    setTableBC();
    $("#course_table tbody").click(dealCourseTable);
});
