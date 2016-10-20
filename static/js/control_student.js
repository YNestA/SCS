function setTableBC() {
    $("#student_table tbody tr:odd,#student_table tbody tr:odd input.score_input").css("background-color","#f6f4f0");
    $("#student_table tbody tr:even,#student_table tbody tr:even input.score_input").css("background-color","#fff");
}
function modifyScore($target) {
    var $scoreInput=$target.closest("tr").find("input.score_input");
    //var old_color=$scoreInput.css("background-color");
    var old_value=$scoreInput.val();
    $scoreInput.unbind("focus",myBlur).attr("readonly",false).addClass("in_modify").focus();
    $("html,body").click(function (event) {
        if(!$(event.target).hasClass("in_modify")) {
            $scoreInput.focus(myBlur).attr("readonly", true).removeClass("in_modify");
            if ($scoreInput.val() !== old_value) {
                $scoreInput.addClass("after_modify");
            }
            ;
            $("html,body").unbind("click", arguments.callee);
        }
    });
}
function submitScore(){
    $("html").click();
    var $inputs=$("input.after_modify");
    for(var i=0;i<$inputs.length;i++){
        var $theInput=$inputs.eq(i);
        if(!(/^((\d{1,2}(\.\d+)?)|100)$/.test($theInput.val())||/^100$/.test($theInput.val()))){
            $theInput.addClass("error_score");
        }else {
            $theInput.removeClass("error_score");
        };
    }
    console.log($("input.error_score").length);
    if($("input.error_score").length){
        $.myAlert("成绩格式有误");
    }else{
        var records=[]
        $inputs.each(function () {
            records.push({"record_id":$(this).closest("tr").attr("data-id"),"score":$(this).val()})
        }) ;
        $.myConfirm({
            message:"确定提交成绩吗？",
            trueCallback:function () {
                $.ajax({
                    type: "POST",
                    url:"/SCS/modify_score/",
                    data:JSON.stringify({"records":records}),
                    success:function (data,textStatus) {
                        var jsonDict=eval("("+data+")");
                        if(jsonDict["res"]==="success"){
                            $.myAlert("提交成功");
                        }else if(jsonDict["res"]==="fail"){
                            $.myAlert("提交失败");
                        }
                    },
                })
            }
        });
    }
}
function dealStudentTable(event) {
    var $target=$(event.target);
    if($target.hasClass("modify_score_btn")){
        modifyScore($target);
        event.stopPropagation();
    }else if($target.hasClass("submit_score_btn")){
        submitScore();
    }
}
function myBlur(event) {
    $(this).blur();
}
$(document).ready(function () {
    $("#left_arrow").detach().appendTo($("#left ul li:eq(2)"));
    setTableBC();
    $("input.score_input").focus(myBlur);
    $("#student_table tbody").click(dealStudentTable);
});
