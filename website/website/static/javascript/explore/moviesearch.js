function ajoutActors (actor) {

    if(!actor.name=="") {
    var superior = document.getElementById("actors").getElementsByTagName("ul")[0];

    var father = document.createElement('li');
    father.className="listactor";

    
    var paragraph = document.createElement('p');
    paragraph.className="actor";
    paragraph.id = actor.imdb_id;
  

    
    var check = document.createElement('input');
    check.type="checkbox";
    check.name="actor";
    check.value="???";

    var name = document.createElement('span');
    name.className="name";

    var text = actor.name;
    name.appendChild(document.createTextNode(text));
    


    paragraph.appendChild(check);
    paragraph.appendChild(name);

    
    father.appendChild(paragraph);
    superior.appendChild(father);


        $(check).each(function () {
        var self = $(this),
        label = self.next(),
        label_text = label.text();
        label.remove();
        self.iCheck({
            checkboxClass: 'icheckbox_line-red',
            radioClass: 'iradio_line-red',
            insert: '<div class="icheck_line-icon"></div>' + label_text
        })
    });

    element = document.getElementById(actor.imdb_id).getElementsByClassName('iCheck-helper')[0];
    element.onclick=function(){changement();};
	}
};



function ajoutTabActors (actors) {
    for (k=0;k<actors.length;k++) {
        ajoutActors(actors[k]);
    };
};

function ajoutDirectors (director) {
    
    var superior = document.getElementById("directors").getElementsByTagName("ul")[0];

    var father = document.createElement('li');
    father.className="listdirector";

    
    var paragraph = document.createElement('p');
    paragraph.className="director";
    paragraph.id = director.imdb_id;
  

    
    var check = document.createElement('input');
    check.type="checkbox";
    check.name="director";
    check.value="???";

    var name = document.createElement('span');
    name.className="name";

    var text = director.name;
    name.appendChild(document.createTextNode(text));

    paragraph.appendChild(check);
    paragraph.appendChild(name);
 
    father.appendChild(paragraph);
    superior.appendChild(father);
    
        $(check).each(function () {
        var self = $(this),
        label = self.next(),
        label_text = label.text();
        label.remove();
        self.iCheck({
            checkboxClass: 'icheckbox_line-red',
            radioClass: 'iradio_line-red',
            insert: '<div class="icheck_line-icon"></div>' + label_text
        })
    });

    element = document.getElementById(director.imdb_id).getElementsByClassName('iCheck-helper')[0];
    element.onclick=function(){changement();};
};


function ajoutTabDirectors (directors) {
    for (k=0;k<directors.length;k++) {
        
        ajoutDirectors(directors[k]);
    };
};



function ajoutGenres (genre) {
    var superior = document.getElementById("genres").getElementsByTagName("ul")[0];

    var father = document.createElement('li');
    father.className="listgenre";

    
    var paragraph = document.createElement('p');
    paragraph.className="genre";
    paragraph.id = "id_genre_"+genre;
    
    var check = document.createElement('input');
    check.type="checkbox";
    check.name="genre";
    check.value="???";

    var name = document.createElement('span');
    name.className="name";

    var text = genre;
    name.appendChild(document.createTextNode(text));
    

    paragraph.appendChild(check);
    paragraph.appendChild(name);

    
    father.appendChild(paragraph);
    superior.appendChild(father);


        $(check).each(function () {
        var self = $(this),
        label = self.next(),
        label_text = label.text();
        label.remove();
        self.iCheck({
            checkboxClass: 'icheckbox_line-red',
            radioClass: 'iradio_line-red',
            insert: '<div class="icheck_line-icon"></div>' + label_text
        });
    });

    element = document.getElementById("id_genre_"+genre).getElementsByClassName('iCheck-helper')[0];
    element.onclick=function(){changement();};
};

function ajoutTabGenres (genres) {
    for (k=0;k<genres.length;k++) {
        ajoutGenres(genres[k]);
    };
};

              
                /*<li class="listactor">
                    <p class="actor">
                    <input type="checkbox" name="actor" value="actor1">
                    <span class="name">Cate Blanchett</span>
                    </p>                       
                </li>*/
	
/*function ajoutBudget (budget) {
   var slider = document.getElementById('slider-range');
   var budgetInM = budget/100000
   $(slider).slider( "option", "values", [budgetInM,budgetInM] );
   var amount = document.getElementById('amount');
   $(amount).val( "$" + budgetInM + "M - $" + budgetInM +"M" );

   };

function ajoutDate (date) {
    var amountyear = document.getElementById('amountyear');
    $(amountyear).val( date );
    };*/
    


$(document).ready(function() {
    var isSubmitted = false;
    
    $('body').on('change', '.autocomplete-light-widget select[name$=title_original]', function() {
        
        if (!isSubmitted) {
            isSubmitted = true;
            var film = $('#id_title_original');
            var film_name = $('#id_title_original-deck').clone().children().children().remove().end().text();
	    var film_imdb_id = $('#id_title_original-deck span.div').attr('data-value');

            var ul = document.getElementById("actors").getElementsByTagName("ul")[0];
            var ul2 = document.getElementById("genres").getElementsByTagName("ul")[0];
			var ul3 = document.getElementById("directors").getElementsByTagName("ul")[0];
            
            if (ul.hasChildNodes())
           {
               while (ul.childNodes.length>=1)
               {ul.removeChild(ul.firstChild);
                }
               };
             if (ul2.hasChildNodes())
           {
               while (ul2.childNodes.length>=1)
               {ul2.removeChild(ul2.firstChild);
                }
               };
			  if (ul3.hasChildNodes())
           {
               while (ul3.childNodes.length>=1)
               {ul3.removeChild(ul3.firstChild);
                }
               };

        function affichage(film_id) {           
              $.post("/cinema/filmInfo/","film_id="+film_id,function(data){ajoutTabActors(data.actors);
                                                                           ajoutTabGenres(data.genres);ajoutTabDirectors(data.directors);});
              };

              
        //$.post("/cinema/getId/","film_name="+film_name,function(data){affichage(data);});
		affichage(film_imdb_id);
        changement2();
            }
        
        else {
            isSubmitted = false;
            
            var ul = document.getElementById("actors").getElementsByTagName("ul")[0];
            var ul2 = document.getElementById("genres").getElementsByTagName("ul")[0];
			var ul3 = document.getElementById("directors").getElementsByTagName("ul")[0];
            
            if (ul.hasChildNodes())
           {
               while (ul.childNodes.length>=1)
               {ul.removeChild(ul.firstChild);
                }
               };
             if (ul2.hasChildNodes())
           {
               while (ul2.childNodes.length>=1)
               {ul2.removeChild(ul2.firstChild);
                }
               };
			 if (ul3.hasChildNodes())
           {
               while (ul3.childNodes.length>=1)
               {ul3.removeChild(ul3.firstChild);
                }
               };

            
            };
        });
    });
            
            
            

