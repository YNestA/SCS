function setTableBC() {
    $("#course_table tbody tr:odd").css("background-color","#f6f4f0");
    $("#course_table tbody tr:even").css("background-color","#fff");
}

function dealCourseTable(event){
    var $target=$(event.target);
    if($target.hasClass("look_lt_btn")){
        deallookLT(event,$target);
    }
}

$(document).ready(function () {
   $("#left_arrow").detach().appendTo($("#left ul li:eq(1)"));
    setTableBC();
    $("#course_table tbody").click(dealCourseTable);
});
