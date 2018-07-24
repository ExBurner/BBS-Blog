// 实现后台管理界面标签页的点击切换效果，根据不同的条件从服务器获取对应的信息，例如传入分类则获取所有分类信息
function active(ele) {
    ele.addClass("active").siblings().removeClass("active");
    $.ajax({
        url: "/back_stage_list/",
        type: "GET",
        data: {
            "id": ele.attr("id")
        },
        success: function (data) {
            $("#backstage_content").html(data);
        }
    })
}

$("#backstage_article").click(function () {
    location.href = "/back_stage";
});
$("#backstage_sort").click(function () {
    active($(this));
});
$("#backstage_tag").click(function () {
    active($(this))
});


// 用户更改密码
$("#change_password").click(function () {
    $.ajax({
        url: "/change_password/",
        type: "POST",
        data: {
            "old_password": $("#old_password").val(),
            "new_password": $("#new_password").val(),
            "re_password": $("#re_password").val()
        },
        success: function (data) {
            if (data) {
                $("#error").html(data)
            }
            else {
                alert("修改成功！点击确认重新登录");
                location.href = "/login/"
            }
        }
    })
});

