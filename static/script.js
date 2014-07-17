document.addEventListener("DOMContentLoaded", function(event) {
    var req = new XMLHttpRequest();
    req.open('get', '/ping', true);
    req.onreadystatechange = function () {
        if(req.readyState == 4) {
            if(req.status == 200) {
                var data = JSON.parse(req.responseText);
                for(var group_name in data.targets) {
                    var group = data.targets[group_name];
                    for(var name in group) {
                        var status = group[name].status;
                        var element = document.querySelectorAll(".status[data-group='" + group_name + "'][data-name='" + name + "']")[0];
                        if(status) {
                            element.className += " true";
                        } else {
                            element.className += " false";
                        }
                    }
                }
            }
        }
    }
    req.send();
});