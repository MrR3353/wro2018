$(function() {

	setInterval(function(){

        var oldData_field     = 0;
        var oldData_EVA_field = 0;
        var oldData_ROB_field = 0;

        // Построение основного поля
        oldData_field     = fill_field("field_default", oldData_field);

        // Построение поля Евы
        oldData_EVA_field = fill_field("field_eva", oldData_EVA_field);
        fill_robot("eva")

        // Построение поля Роба
        oldData_ROB_field = fill_field("field_rob", oldData_ROB_field);
        fill_robot("rob")
    }, 500);

});

function fill_robot(name){
    $.getJSON('data/' + name + '.json', function(data){
        var coord = data[0]
        var alpha = data[1]
        $('.' + name).remove();
        var cell = document.getElementsByClassName('.field_' + name + '>.cell-' + coord);
        console.log("<div class='robot " + name + "'></div>")
        $('.field_' + name + '>.cell-' + coord).append("<div class='robot " + name + "'></div>");
        
        $('.' + name).addClass("rotate" + alpha);
        console.log($('.field_' + name + '>.cell-' + coord + ">." + name))
    });
}

function fill_field(field, oldData){
    return $.getJSON('data/' + field + '.json', function(data){

        var coords = Object.keys(data);
        if(oldData != data){
            clearField(field) 
        }

        coords.forEach( function(coord){
            var dir = data[coord] 

            if (~dir.indexOf("r")){
                $("." + field + ">.cell-" + coord + ">.r").css("opacity",1);
            }else{
                $("." + field + ">.cell-" + coord + ">.r").css("opacity",0);
            }

            if (~dir.indexOf("t")){
                $("." + field + ">.cell-" + coord + ">.t").css("opacity",1);
            }else{
                $("." + field + ">.cell-" + coord + ">.t").css("opacity",0);
            }

            if (~dir.indexOf("l")){
                $("." + field + ">.cell-" + coord + ">.l").css("opacity",1);
            }else{
                $("." + field + ">.cell-" + coord + ">.l").css("opacity",0);
            }

            if (~dir.indexOf("b")){
                $("." + field + ">.cell-" + coord + ">.b").css("opacity",1);
            }else{
                $("." + field + ">.cell-" + coord + ">.b").css("opacity",0);
            }
        });
        return data; 
    });
}

function clearField(field){ 
    for(var x = 0; x < 5; x++){
        for(var y = 1; y < 6; y++){
            $("." + field + ">.cell-" + x.toString() + y.toString() + ">.r").css("opacity", 0)
            $("." + field + ">.cell-" + x.toString() + y.toString() + ">.t").css("opacity", 0)
            $("." + field + ">.cell-" + x.toString() + y.toString() + ">.l").css("opacity", 0)
            $("." + field + ">.cell-" + x.toString() + y.toString() + ">.b").css("opacity", 0)
        }
    }
}