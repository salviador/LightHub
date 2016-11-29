function popola_nodi(data) {



    console.log('*****POPOLA NODI**********');
    console.log(data);
    console.log('**************************');

    $('#NodiTable > tbody').append('<tr id="Nodo_' + Object.keys(data)[0] + '" style="background-color:azure"> <td>'
        + Object.keys(data)[0] + '</td> <td>' + data[Object.keys(data)[0]].Descrizione + 
        
        '</td> <td>online</td> <td> <table border="0" cellspacing="5" cellpadding="5" align="center" width="100%"> \
        <thead> \
        <tr> \
        <th width="25%"> <p>CH1</p><span style="font-size:0.8em"> [x]Enable dimmer</span><br /> <span style="font-size:0.8em"> [ ]Only switch</span></th> \
        <th width="25%"> <p>CH2</p><span style="font-size:0.8em"> [x]Enable dimmer</span><br /> <span style="font-size:0.8em"> [ ]Only switch</span></th> \
        <th width="25%"> <p>CH3</p><span style="font-size:0.8em"> [x]Enable dimmer</span><br /> <span style="font-size:0.8em"> [ ]Only switch</span></th> \
        <th width="25%"> <p>CH4</p><span style="font-size:0.8em"> [x]Enable dimmer</span><br /> <span style="font-size:0.8em"> [ ]Only switch</span></th> \
        </tr> \
        </thead> \
        <tbody> \
        <tr> \
        <td><input class="dimmerCheckbox" id="Checkbox1" type="checkbox" /></td> \
        <td><input class="dimmerCheckbox" id="Checkbox2" type="checkbox" /></td> \
        <td><input class="dimmerCheckbox" id="Checkbox3" type="checkbox" /></td> \
        <td><input class="dimmerCheckbox" id="Checkbox4" type="checkbox" /></td> \
        </tr> \
        </tbody> \
        </table> \
        </td> <td><button type="button" class="btn btn-secondary btn-primary rowUp">Up</button></td><td><button type="button" class="btn btn-secondary btn-primary rowDown">Down</button></td> \
        <td><button type="button" id="nodi_remove_' + Object.keys(data)[0] + '" class="btn btn-secondary btn-danger rowRemove">Elimina</button></td> </tr>');



}


function popola_nodi_setting_dimmer(key, val) {
    console.log(key);
    console.log(val);
    console.log(val.Ordine);
    console.log(val.funzionamento[0].ch1);
    console.log(val.funzionamento[0].ch2);
    console.log(val.funzionamento[0].ch3);
    console.log(val.funzionamento[0].ch4);

    var ch1checked = "";
    if (val.funzionamento[0].ch1 === "true") {
        ch1checked = 'checked = "checked"';
    }
    var ch2checked = "";
    if (val.funzionamento[0].ch2 === "true") {
        ch2checked = 'checked = "checked"';
    }
    var ch3checked = "";
    if (val.funzionamento[0].ch3 === "true") {
        ch3checked = 'checked = "checked"';
    }
    var ch4checked = "";
    if (val.funzionamento[0].ch4 === "true") {
        ch4checked = 'checked = "checked"';
    }


    $('#NodiTable > tbody').append('<tr id="Nodo_' + key + '" style="background-color:azure"> <td>'
        + key + '</td> <td>' + val.Descrizione +

        '</td> <td>online</td> <td> <table border="0" cellspacing="5" cellpadding="5" align="center" width="100%"> \
        <thead> \
        <tr> \
        <th width="25%"> <p>CH1</p><span style="font-size:0.8em"> [x]Enable dimmer</span><br /> <span style="font-size:0.8em"> [ ]Only switch</span></th> \
        <th width="25%"> <p>CH2</p><span style="font-size:0.8em"> [x]Enable dimmer</span><br /> <span style="font-size:0.8em"> [ ]Only switch</span></th> \
        <th width="25%"> <p>CH3</p><span style="font-size:0.8em"> [x]Enable dimmer</span><br /> <span style="font-size:0.8em"> [ ]Only switch</span></th> \
        <th width="25%"> <p>CH4</p><span style="font-size:0.8em"> [x]Enable dimmer</span><br /> <span style="font-size:0.8em"> [ ]Only switch</span></th> \
        </tr> \
        </thead> \
        <tbody> \
        <tr> \
        <td><input class="dimmerCheckbox" id="Checkbox1" type="checkbox" ' + ch1checked + ' /></td> \
        <td><input class="dimmerCheckbox" id="Checkbox2" type="checkbox" ' + ch2checked + ' /></td> \
        <td><input class="dimmerCheckbox" id="Checkbox3" type="checkbox" ' + ch3checked + ' /></td> \
        <td><input class="dimmerCheckbox" id="Checkbox4" type="checkbox" ' + ch4checked + ' /></td> \
        </tr> \
        </tbody> \
        </table> \
        </td> <td><button type="button" class="btn btn-secondary btn-primary rowUp">Up</button></td><td><button type="button" class="btn btn-secondary btn-primary rowDown">Down</button></td> \
        <td><button type="button" id="nodi_remove_' + key + '" class="btn btn-secondary btn-danger rowRemove">Elimina</button></td> </tr>');
}