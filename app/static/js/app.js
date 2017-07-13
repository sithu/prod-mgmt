var refInterval = window.setInterval('update()', 30000); // 30 seconds

var update = function() {
    $.ajax({
        type : 'GET',
        url : '../api/dashboard',
        success : function(data){
            console.log(data);
        },
    });
};
