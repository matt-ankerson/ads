
function cracker(base, dictionary) {
    // _ indicates missing character.
    // + indicates letters that must be the same.
    // words in dictionary are considered to be the right lenth.
    // example: __z+__+
};


$(document).ready(function() {

    $("#btn_calculate").on("click", function(e){

        // Get the html input's contents.
        var base_word = $("#base_input").val().toLowerCase();
        
        // Get the dictionary, located on the server.
        $.ajax({
            url: "http://localhost:5555/lexicon_data/words.txt",
            success: function(response) {
                var dictionary = response.split("\n");

                // Clean the dictionary
                for(var i = 0; i < dictionary.length; i++) {
                    dictionary[i] = dictionary[i].toLowerCase()
                                        .replace(/[^\w\s]|_/g, "")
                                        .replace(/\s+/g, " ");
                }

                console.log(dictionary[0]);
                console.log(dictionary[1]);
                console.log(dictionary[2]);
                console.log(dictionary[3]);

                // Run the function, push the output to the DOM.
            },
            error: function(error) {
                alert("Could not load dictionary file. " + error.toString());
            }
        });

    });
});
