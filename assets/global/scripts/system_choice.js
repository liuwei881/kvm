String.format = function() {
    var s = arguments[0];
    for (var i = 0; i < arguments.length - 1; i++) {
    var reg = new RegExp("\\{" + i + "\\}", "gm");
    s = s.replace(reg, arguments[i + 1]);
    }
    return s;
    }

$(function(){
        $.ajax({
            type:'POST',
            url:'/get_system/',
            data:{"parent":0,"level":1},
            success:function(data){
                var all_ps=data['dict_system']
                for(var i=0;i<all_ps.length;i++){
                    var $html=String.format('<option value="{0}">{1}</option>',all_ps[i][0],all_ps[i][1])
                    $('#system').append($html)
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("error");
                    },
            dataType: 'json'
        });

        $('#system').change(function(){
            var parent = $('#system').val()
            $.ajax({
            type:'POST',
            url:'/get_system/',
            data:{"parent":parent,"level":2},
            success:function(data){
                var all_ps=data['dict_system']
                var $mirror_name = $('#mirror_name').empty();
                $mirror_name.append('<option selected value="">选择一个镜像</option>')
                for(var i=0;i<all_ps.length;i++){
                    var $html=String.format('<option value="{0}">{1}</option>',all_ps[i][1],all_ps[i][1])
                    $('#mirror_name').append($html)
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("error");
                    },
            dataType: 'json'
        });
        })
        })