// Lien entre genre1 et keywords

//$.ajaxSetup( {headers : {"X-Requested-With" : "Ajax"}});

$(document).ready(function() {
	var dict={};
    $('body').on('change', '.autocomplete-light-widget select[name$=genre1]', function() {
        var genre1SelectElement = $(this);
        var keywordSelectElement = $('#' + $(this).attr('id').replace('genre1', 'keyword'));
        var keywordWidgetElement = keywordSelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            dict['genre1_id'] = value[0];
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        } else {
            // If value is empty, empty autocomplete.data
            dict['genre1_id'] = -2;
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(keywordWidgetElement, 'data is', keywordWidgetElement.yourlabsWidget().autocomplete.data)
    })

// Lien entre genre2 et keywords

    $('body').on('change', '.autocomplete-light-widget select[name$=genre2]', function() {
        var genre2SelectElement = $(this);
        var keywordSelectElement = $('#' + $(this).attr('id').replace('genre2', 'keyword'));
        var keywordWidgetElement = keywordSelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            dict['genre2_id'] = value[0];
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        } else {
            // If value is empty, empty autocomplete.data
            dict['genre2_id'] = -2;
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(keywordWidgetElement, 'data is', keywordWidgetElement.yourlabsWidget().autocomplete.data)
    })
});

// Lien entre de genre 1 vers genre 2

$(document).ready(function() {
    $('body').on('change', '.autocomplete-light-widget select[name$=genre1]', function() {
        var genre1SelectElement = $(this);
        var genre2SelectElement = $('#' + $(this).attr('id').replace('genre1', 'genre2'));
        var genre2WidgetElement = genre2SelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            genre2WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre1_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            genre2WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre1_id': -2,
            };
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(genre2WidgetElement, 'data is', genre2WidgetElement.yourlabsWidget().autocomplete.data)
    })
});

// Lien entre de genre 2 vers genre 1

$(document).ready(function() {
    $('body').on('change', '.autocomplete-light-widget select[name$=genre2]', function() {
        var genre2SelectElement = $(this);
        var genre1SelectElement = $('#' + $(this).attr('id').replace('genre2', 'genre1'));
        var genre1WidgetElement = genre1SelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            genre1WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre2_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            genre1WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre2_id': -2,
            };
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(genre1WidgetElement, 'data is', genre1WidgetElement.yourlabsWidget().autocomplete.data)
    })
});



function ajoutKeywordSuggest(keyword) {
    var newKeyword = document.createElement('span');
    newKeyword.className="newKeyword";


    var newName = document.createElement('span');
    newName.className="name";

    newName.appendChild(document.createTextNode(keyword));

    var newDelete = document.createElement('span');                               
    newDelete.className="delete";

    var newImg1 = document.createElement('img');
    newImg1.className="add1";
    newImg1.src="../static/img/prediction/AddGrey.png";
   

    var newImg2 = document.createElement('img');
    newImg2.className="add2"; 
    newImg2.src="../static/img/prediction/AddBlue.png";

    keywordClick(newImg1);
    newKeyword.appendChild(newDelete);
    newKeyword.appendChild(newName);

    newDelete.appendChild(newImg1);
    newDelete.appendChild(newImg2);

    document.getElementById("keywordSuggest").appendChild(newKeyword);

};

function keywordClick (icone) {
    $(icone).click(function(){
        if((this.className=="remove div")&&(this.id=="suggest")){
  
            var element = this.parentNode;
            var remove = document.createElement('span');
            var newImg1 = document.createElement('img');
            var newDelete = document.createElement('span');                               
            newDelete.className="delete";
            newImg1.className="add1";
            newImg1.src="../static/img/prediction/AddGrey.png";
            var newImg2 = document.createElement('img');
            newImg2.className="add2"; 
            newImg2.src="../static/img/prediction/AddBlue.png";
            var newName = document.createElement('span');
            var suggestion = document.getElementById("keywordSuggest");
            
            newName.className="name";

            newName.appendChild(document.createTextNode(element.textContent));
            
            this.parentNode.parentNode.removeChild(element);

            if (element.hasChildNodes()){
                     while (element.childNodes.length>=1)
                         {element.removeChild(element.firstChild);
                    }
               };
           

            element.className="newKeyword";
            newDelete.appendChild(newImg1);
            newDelete.appendChild(newImg2);
            element.appendChild(newDelete);
            element.appendChild(newName);
            
            suggestion.appendChild(element);
            keywordClick(newImg1);
            }

        else {
            if (this.className=="remove div") {
            this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);
               }
            else {
                var element = this.parentNode.parentNode;
                var remove = document.createElement('span');
                var text = document.createTextNode(element.getElementsByClassName("name")[0].textContent);
                //var xxx = document.createTextNode("X");
                var keywords = document.getElementById("id_keyword-deck");

                this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);

                if (element.hasChildNodes()){
                     while (element.childNodes.length>=1)
                         {element.removeChild(element.firstChild);
                    }
               };

                remove.className="remove div";
                remove.id="suggest";
                element.className="div hilight";
              
                //remove.appendChild(xxx);
                element.appendChild(remove);
                element.appendChild(text);
                keywords.appendChild(element);

                keywordClick(remove);

                };
            };

    });
};


function callback_suggest (resp) {
    if (resp.success) {
        for (k=0; k<resp.results.length; k++) {
            ajoutKeywordSuggest(resp.results[k][1]);
        }
    }
    else {
        alert('Error : ' + resp.error);
    }
}


$(document).ready(function() {

    $('body').on('change', '.autocomplete-light-widget select[name$=genre1]', function() {
        var genre1 = $('#id_genre1');
        var genre2 = $('#id_genre2');
        var id1 = genre1.val();
        var id2 = genre2.val();
        urlSubmit = 'http://www.prodbox.co/learning/suggest/';
	var bloc = document.getElementById("keywordSuggest");

        if (id1) {
            var value1 = $('#id_genre1-deck').clone().children().children().remove().end().text();

          
        
            if (id2) {
                var value2 = $('#id_genre2-deck').clone().children().children().remove().end().text();
				
                if (bloc.hasChildNodes()) {
                    while (bloc.childNodes.length>=1)
                    {bloc.removeChild(bloc.firstChild);
                }
               };				
				
				
				 var args1 = {'str' : '', 'nbresults' : 5, filter:[[1.0, value1]]};
				 var args2 = {'str' : '', 'nbresults' : 5, filter:[[1.0, value2]]};
				 $.post(urlSubmit, "json_request="+JSON.stringify(args1), callback_suggest, "json");
				 $.post(urlSubmit, "json_request="+JSON.stringify(args2), callback_suggest, "json");
			
				
                
                }
            else {
               var args = {'str' : '', 'nbresults' : 10, filter:[[1.0, value1]]};
			   if (bloc.hasChildNodes()) {
               while (bloc.childNodes.length>=1)
               {bloc.removeChild(bloc.firstChild);
                }
               };
              
               $.post(urlSubmit, "json_request="+JSON.stringify(args), callback_suggest, "json");
	
	                  
                };
            }
        else {if (id2) {
            var value2 = $('#id_genre2-deck').clone().children().children().remove().end().text();
			var args = {'str' : '', 'nbresults' : 10, filter:[[1.0, value2]]};
            
			
			
				if (bloc.hasChildNodes()) {
				 while (bloc.childNodes.length>=1)
                 {bloc.removeChild(bloc.firstChild);
                }
               };
			   
			  $.post(urlSubmit, "json_request="+JSON.stringify(args), callback_suggest, "json");
			   
	
                };
			};
		});
		
		$('body').on('change', '.autocomplete-light-widget select[name$=genre2]', function() {
        var genre1 = $('#id_genre1');
        var genre2 = $('#id_genre2');
        var id1 = genre1.val();
        var id2 = genre2.val();
        urlSubmit = 'http://www.prodbox.co/learning/suggest/';
		var bloc = document.getElementById("keywordSuggest");

        if (id1) {
            var value1 = $('#id_genre1-deck').clone().children().children().remove().end().text();

          
        
            if (id2) {
                var value2 = $('#id_genre2-deck').clone().children().children().remove().end().text();
				
				 if (bloc.hasChildNodes()) {
				 while (bloc.childNodes.length>=1)
                 {bloc.removeChild(bloc.firstChild);
                }
               };				
				
				
				var args1 = {'str' : '', 'nbresults' : 5, filter:[[1.0, value1]]};
				var args2 = {'str' : '', 'nbresults' : 5, filter:[[1.0, value2]]};
				$.post(urlSubmit, "json_request="+JSON.stringify(args1), callback_suggest, "json");
				$.post(urlSubmit, "json_request="+JSON.stringify(args2), callback_suggest, "json");
			
				
                
                }
            else {
               var args = {'str' : '', 'nbresults' : 10, filter:[[1.0, value1]]};
			   if (bloc.hasChildNodes()) {
               while (bloc.childNodes.length>=1)
               {bloc.removeChild(bloc.firstChild);
                }
               };
              
              $.post(urlSubmit, "json_request="+JSON.stringify(args), callback_suggest, "json");


	                  
                };
            }
        else {if (id2) {
            var value2 = $('#id_genre2-deck').clone().children().children().remove().end().text();
			var args = {'str' : '', 'nbresults' : 10, filter:[[1.0, value2]]};
            
			
			
				if (bloc.hasChildNodes()) {
				 while (bloc.childNodes.length>=1)
                 {bloc.removeChild(bloc.firstChild);
                }
               };
			   
			  $.post(urlSubmit, "json_request="+JSON.stringify(args), callback_suggest, "json");

                };
			};
		});
	});
				
				
	/*
$(document).ready(function() {
	
    $('body').on('change', '.autocomplete-light-widget select[name$=actors]', function() {
        var actor = $('#id_actors');
        var pourId = document.getElementById('id_actors-deck').lastChild;
        pourId.removeChild(pourId.firstChild);
        var name = pourId.textContent;
        alert(name + " " + pourId.getAttribute("imdb-id"));

        $.post("/cinema/getIdActor/","actor_name="+name,function(data){pourId.id=data});
        });
    });
   */
