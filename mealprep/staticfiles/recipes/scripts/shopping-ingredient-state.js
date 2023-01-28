// Change background of ingredients to green to mark them as bought. Log ingredient status changes to the model.
$(document).ready(function(){
    $("[data-id='ingredient']").on("click", function(){
        var ingredient_id= $(this).attr("data-ingredient-id");
        var ingredient_class = $('[data-ingredient-id="ingredient_' + ingredient_id + '"]').attr("class");

        if (ingredient_class == "card shadow-sm h-100 justify-content-center align-items-center") {
            var card_class = "card shadow-sm h-100 justify-content-center align-items-center border border-2 border-success";
            var action = '1';
            var background = "rgba(228,250,191,255)";
        } else {
            var card_class = "card shadow-sm h-100 justify-content-center align-items-center";
            var action = '0';
            var background = "white";
        };

        $('[data-ingredient-id="ingredient_' + ingredient_id + '"]').attr("class", card_class);
        $('[data-ingredient-id="ingredient_' + ingredient_id + '"]').attr("style", "background: ".concat(background));
            $.post({
                url: "/shopping_update",
                headers: { "X-CSRFToken": $.cookie("csrftoken") },
                'data': {
                    'action': action,
                    'ingredient_id': ingredient_id,
                },
                success: function ( data ) {
                }
            });
        return false;
    });
});
