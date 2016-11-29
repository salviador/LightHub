function popola_main_nodi_dimmer(nodo, val) {

    /*
    console.log('*****POPOLA NODI**********');
    console.log(val.disable);
    console.log('----------------------------');
    */
    //console.log(val.stato[0].ch1b);
    //console.log((val.stato[0].ch1b).localeCompare("true"));
    //console.log('**************************');

    //console.log(val.stato[0].ch1b);
    var checked1 = "";
    var lamp1 = "";
    if (((val.stato[0].ch1b).localeCompare("true"))==0) {      //da verificare
        lamp1 = "/WebSite1/image/lamp_accesa.svg";
        checked1 = "checked";
    } else {
        lamp1 = "/WebSite1/image/lamp_spenta.svg";
        checked1 = "";
        //console.log("false");
    }
    var checked2 = "";
    var lamp2 = "";
    if (((val.stato[0].ch2b).localeCompare("true")) == 0) {     //da verificare
        lamp2 = "/WebSite1/image/lamp_accesa.svg";
        checked2 = "checked";
    } else {
        lamp2 = "/WebSite1/image/lamp_spenta.svg";
        checked2 = "";
    }
    var checked3 = "";
    var lamp3 = "";
    if (((val.stato[0].ch3b).localeCompare("true")) == 0) {      //da verificare
        lamp3 = "/WebSite1/image/lamp_accesa.svg";
        checked3 = "checked";
    } else {
        lamp3 = "/WebSite1/image/lamp_spenta.svg";
        checked3 = "";
    }
    var checked4 = "";
    var lamp4 = "";
    if (((val.stato[0].ch4b).localeCompare("true")) == 0) {     //da verificare
        lamp4 = "/WebSite1/image/lamp_accesa.svg";
        checked4 = "checked";
    } else {
        lamp4 = "/WebSite1/image/lamp_spenta.svg";
        checked4 = "";
    }

    
    $('#body_NODI').append(' \
        <div id="nodo_' + nodo + '" class="panel panel-default" style="box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.14), 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 1px 5px 0 rgba(0, 0, 0, 0.12);"> \
                            <div class="panel-heading">' + nodo + '</div> \
                            <div class="panel-body central_panel_nodo_enable"> \
                            <table style="border-collapse:separate; border-spacing:1em;" id="nodo_' + nodo + '" border="0" cellspacing="5" cellpadding="5" align="center"> \
                                <tbody> \
                                    <tr> \
                                        <th width="5%"> \
                                            <span class="mdl-form__icon"> \
                                                <img id="nodo_' + nodo + '_ch1" data-icon="switch" src="' + lamp1 + '" style="width:32px;"> \
                                            </span> \
                                        </th> \
                                        <th width="50%"> \
                                            <span class="mdl-form__label" style="padding-left:30px;">Ch 1 </span> \
                                        </th> \
                                        <th width="40%"> \
                                            <input id="nodo_' + nodo + '_ch1" class="slider" data-slider-id="ex1Slider" type="text" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="' + val.stato[0].ch1d + '" /> \
                                        </th> \
                                        <th align="right" width="5%"> \
                                            <input ' + checked1 + ' id="nodo_' + nodo + '_ch1" class="switch" data-toggle="toggle" data-width="100" type="checkbox"> \
                                       </th> \
                                    </tr> \
                                    <tr> \
                                        <th width="5%"> \
                                            <span class="mdl-form__icon"> \
                                                <img id="nodo_' + nodo + '_ch2" data-icon="switch" src="' + lamp2 + '" style="width:32px;"> \
                                            </span> \
                                        </th> \
                                        <th width="50%"> \
                                            <span class="mdl-form__label" style="padding-left:30px;">Ch 2 </span> \
                                        </th> \
                                        <th width="40%"> \
                                            <input id="nodo_' + nodo + '_ch2" class="slider" data-slider-id="ex1Slider" type="text" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="' + val.stato[0].ch2d + '" /> \
                                        </th> \
                                        <th align="right" width="5%"> \
                                            <input ' + checked2 + ' id="nodo_' + nodo + '_ch2" class="switch" data-toggle="toggle" data-width="100" type="checkbox"> \
                                       </th> \
                                    </tr>  \
                                    <tr> \
                                        <th width="5%"> \
                                            <span class="mdl-form__icon"> \
                                                <img id="nodo_' + nodo + '_ch3" data-icon="switch" src="' + lamp3 + '" style="width:32px;"> \
                                            </span> \
                                        </th> \
                                        <th width="50%"> \
                                            <span class="mdl-form__label" style="padding-left:30px;">Ch 3 </span> \
                                        </th> \
                                        <th width="40%"> \
                                            <input id="nodo_' + nodo + '_ch3" class="slider" data-slider-id="ex1Slider" type="text" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="' + val.stato[0].ch3d + '" /> \
                                        </th> \
                                        <th align="right" width="5%"> \
                                            <input ' + checked3 + ' id="nodo_' + nodo + '_ch3" class="switch" data-toggle="toggle" data-width="100" type="checkbox"> \
                                       </th> \
                                    </tr>  \
                                    <tr> \
                                        <th width="5%"> \
                                            <span class="mdl-form__icon"> \
                                                <img id="nodo_' + nodo + '_ch4" data-icon="switch" src="' + lamp4 + '" style="width:32px;"> \
                                            </span> \
                                        </th> \
                                        <th width="50%"> \
                                            <span class="mdl-form__label" style="padding-left:30px;">Ch 4 </span> \
                                        </th> \
                                        <th width="40%"> \
                                            <input id="nodo_' + nodo + '_ch4" class="slider" data-slider-id="ex1Slider" type="text" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="' + val.stato[0].ch4d + '" /> \
                                        </th> \
                                        <th align="right" width="5%"> \
                                            <input ' + checked4 + ' id="nodo_' + nodo + '_ch4" class="switch" data-toggle="toggle" data-width="100" type="checkbox"> \
                                       </th> \
                                    </tr>  \
                                    ');
    
    
  
    
    $('#' + 'nodo_' + nodo + '_ch1.switch').bootstrapToggle();
    $('#' + 'nodo_' + nodo + '_ch2.switch').bootstrapToggle();
    $('#' + 'nodo_' + nodo + '_ch3.switch').bootstrapToggle();
    $('#' + 'nodo_' + nodo + '_ch4.switch').bootstrapToggle();
  

    $('#' + 'nodo_' + nodo + '_ch1.slider').slider({});
    $('#' + 'nodo_' + nodo + '_ch2.slider').slider({});
    $('#' + 'nodo_' + nodo + '_ch3.slider').slider({});
    $('#' + 'nodo_' + nodo + '_ch4.slider').slider({});


/*
    console.log("PROBLEMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
    console.log($('#nodo_' + nodo + ' .toggle'));

   // $('#nodo_' + nodo + ' .toggle').addClass("switch");
   // $('#nodo_' + nodo + ' .toggle').attr('id', 'nodo_' + nodo );

   */



    if (((val.funzionamento[0].ch1).localeCompare("true")) == 0) {      //da verificare
        $('#' + 'nodo_' + nodo + '_ch1.slider').slider("enable");
    } else {
        $('#' + 'nodo_' + nodo + '_ch1.slider').slider("disable");
        $('#' + 'nodo_' + nodo + '_ch1.slider').slider('setValue', 0);
    }
    if (((val.funzionamento[0].ch2).localeCompare("true")) == 0) {      //da verificare
        $('#' + 'nodo_' + nodo + '_ch2.slider').slider("enable");
    } else {
        $('#' + 'nodo_' + nodo + '_ch2.slider').slider("disable");
        $('#' + 'nodo_' + nodo + '_ch2.slider').slider('setValue', 0);
    }
    if (((val.funzionamento[0].ch3).localeCompare("true")) == 0) {      //da verificare
        $('#' + 'nodo_' + nodo + '_ch3.slider').slider("enable");
    } else {
        $('#' + 'nodo_' + nodo + '_ch3.slider').slider("disable");
        $('#' + 'nodo_' + nodo + '_ch3.slider').slider('setValue', 0);
    }
    if (((val.funzionamento[0].ch4).localeCompare("true")) == 0) {      //da verificare
        $('#' + 'nodo_' + nodo + '_ch4.slider').slider("enable");
    } else {
        $('#' + 'nodo_' + nodo + '_ch4.slider').slider("disable");
        $('#' + 'nodo_' + nodo + '_ch4.slider').slider('setValue', 0);
    }

}


function disable_nodo(nodo) {

    $('#nodo_' + nodo + ' > .panel-body').removeClass('central_panel_nodo_enable').addClass('central_panel_nodo_disable');

    $('#nodo_' + nodo + ' > .panel-heading').addClass('heading_panel_nodo_disable');

    $('img#nodo_' + nodo + '_ch1').attr("src", "/WebSite1/image/lamp_disabilitata.svg");
    $('img#nodo_' + nodo + '_ch2').attr("src", "/WebSite1/image/lamp_disabilitata.svg");
    $('img#nodo_' + nodo + '_ch3').attr("src", "/WebSite1/image/lamp_disabilitata.svg");
    $('img#nodo_' + nodo + '_ch4').attr("src", "/WebSite1/image/lamp_disabilitata.svg");

    $('#nodo_' + nodo + '_ch1.switch').bootstrapToggle('disable');
    $('#nodo_' + nodo + '_ch2.switch').bootstrapToggle('disable');
    $('#nodo_' + nodo + '_ch3.switch').bootstrapToggle('disable');
    $('#nodo_' + nodo + '_ch4.switch').bootstrapToggle('disable');

    $('#nodo_' + nodo + '_ch1.slider').slider('disable');
    $('#nodo_' + nodo + '_ch2.slider').slider('disable');
    $('#nodo_' + nodo + '_ch3.slider').slider('disable');
    $('#nodo_' + nodo + '_ch4.slider').slider('disable');

    //aggiungi bottone "Connetti"
    $('#nodo_' + nodo + ' > .panel-heading').html(nodo + '<div class="btn-group"><a id="' + nodo + '" href="#" class="btn btn-success btn-sm btnAggiungi bottoniConnetti" style="margin-left:10px;">Connetti</a></div>');




}


function abilita_nodo(nodo, funzionamento) {
    $('#nodo_' + nodo + ' > .panel-body').removeClass('central_panel_nodo_disable').addClass('central_panel_nodo_enable');

    $('#nodo_' + nodo + ' > .panel-heading').removeClass('heading_panel_nodo_disable');

    $('img#nodo_' + nodo + '_ch1').attr("src", "/WebSite1/image/lamp_spenta.svg");
    $('img#nodo_' + nodo + '_ch2').attr("src", "/WebSite1/image/lamp_spenta.svg");
    $('img#nodo_' + nodo + '_ch3').attr("src", "/WebSite1/image/lamp_spenta.svg");
    $('img#nodo_' + nodo + '_ch4').attr("src", "/WebSite1/image/lamp_spenta.svg");

    $('#nodo_' + nodo + '_ch1.switch').bootstrapToggle('enable');
    $('#nodo_' + nodo + '_ch2.switch').bootstrapToggle('enable');
    $('#nodo_' + nodo + '_ch3.switch').bootstrapToggle('enable');
    $('#nodo_' + nodo + '_ch4.switch').bootstrapToggle('enable');

    if (((funzionamento.ch1).localeCompare("true")) == 0) {
        $('#nodo_' + nodo + '_ch1.slider').slider('enable');
    }
    if (((funzionamento.ch2).localeCompare("true")) == 0) {
        $('#nodo_' + nodo + '_ch2.slider').slider('enable');
    }
    if (((funzionamento.ch3).localeCompare("true")) == 0) {
        $('#nodo_' + nodo + '_ch3.slider').slider('enable');
    }
    if (((funzionamento.ch4).localeCompare("true")) == 0) {
        $('#nodo_' + nodo + '_ch4.slider').slider('enable');
    }


    //rimuovi bottone "Connetti"
    $('#nodo_' + nodo + ' > .panel-heading > div').remove();

}


function update_command_to_server(nodo) {
    /*
    console.log("ch1 button")
    console.log($('#nodo_' + nodo + '_ch1.switch').closest("input").prop("checked"));
    console.log("ch2 button")
    console.log($('#nodo_' + nodo + '_ch2.switch').closest("input").prop("checked"));
    console.log("ch3 button")
    console.log($('#nodo_' + nodo + '_ch3.switch').closest("input").prop("checked"));
    console.log("ch4 button")
    console.log($('#nodo_' + nodo + '_ch4.switch').closest("input").prop("checked"));

    //slider
    console.log("ch1 slider")
    console.log($('#nodo_' + nodo + '_ch1.slider').closest("input").prop("value"));
    console.log("ch2 slider")
    console.log($('#nodo_' + nodo + '_ch2.slider').closest("input").prop("value"));
    console.log("ch3 slider")
    console.log($('#nodo_' + nodo + '_ch4.slider').closest("input").prop("value"));
    console.log("ch4 slider")
    console.log($('#nodo_' + nodo + '_ch4.slider').closest("input").prop("value"));
    */
    console.log(nodo);

    var json_send_command = {
        "nodo": nodo, "stato":
            {
                "ch1b": ($('#nodo_' + nodo + '_ch1.switch').closest("input").prop("checked")),
                "ch2b": ($('#nodo_' + nodo + '_ch2.switch').closest("input").prop("checked")),
                "ch3b": ($('#nodo_' + nodo + '_ch3.switch').closest("input").prop("checked")),
                "ch4b": ($('#nodo_' + nodo + '_ch4.switch').closest("input").prop("checked")),
                "ch1d": ($('#nodo_' + nodo + '_ch1.slider').closest("input").prop("value")),
                "ch2d": ($('#nodo_' + nodo + '_ch2.slider').closest("input").prop("value")),
                "ch3d": ($('#nodo_' + nodo + '_ch3.slider').closest("input").prop("value")),
                "ch4d": ($('#nodo_' + nodo + '_ch4.slider').closest("input").prop("value"))



            }



    };
    return json_send_command;


}

function update_stato_nodo(nodo, data) {

    $('#' + 'nodo_' + nodo + '_ch1.slider').slider('setValue', data.ch1d);
    $('#' + 'nodo_' + nodo + '_ch2.slider').slider('setValue', data.ch2d);
    $('#' + 'nodo_' + nodo + '_ch3.slider').slider('setValue', data.ch3d);
    $('#' + 'nodo_' + nodo + '_ch4.slider').slider('setValue', data.ch4d);


    if (data.ch1b == 1) {      //da verificare
        $('img#' + 'nodo_' + nodo + '_ch1').attr("src", "/WebSite1/image/lamp_accesa.svg");
        $('#' + 'nodo_' + nodo + '_ch1.switch').bootstrapToggle('on');

    } else {
        $('img#' + 'nodo_' + nodo + '_ch1').attr("src", "/WebSite1/image/lamp_spenta.svg");
        $('#' + 'nodo_' + nodo + '_ch1.switch').bootstrapToggle('off');
    }

    if (data.ch2b == 1) {      //da verificare
        $('img#' + 'nodo_' + nodo + '_ch2').attr("src", "/WebSite1/image/lamp_accesa.svg");
        $('#' + 'nodo_' + nodo + '_ch2.switch').bootstrapToggle('on');

    } else {
        $('img#' + 'nodo_' + nodo + '_ch2').attr("src", "/WebSite1/image/lamp_spenta.svg");
        $('#' + 'nodo_' + nodo + '_ch2.switch').bootstrapToggle('off');
    }
    if (data.ch3b == 1) {      //da verificare
        $('img#' + 'nodo_' + nodo + '_ch3').attr("src", "/WebSite1/image/lamp_accesa.svg");
        $('#' + 'nodo_' + nodo + '_ch3.switch').bootstrapToggle('on');

    } else {
        $('img#' + 'nodo_' + nodo + '_ch3').attr("src", "/WebSite1/image/lamp_spenta.svg");
        $('#' + 'nodo_' + nodo + '_ch3.switch').bootstrapToggle('off');
    }
    if (data.ch4b == 1) {      //da verificare
        $('img#' + 'nodo_' + nodo + '_ch4').attr("src", "/WebSite1/image/lamp_accesa.svg");
        $('#' + 'nodo_' + nodo + '_ch4.switch').bootstrapToggle('on');

    } else {
        $('img#' + 'nodo_' + nodo + '_ch4').attr("src", "/WebSite1/image/lamp_spenta.svg");
        $('#' + 'nodo_' + nodo + '_ch4.switch').bootstrapToggle('off');
    }






}
