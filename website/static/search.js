$("#boat-reg, #phone-number, #boat-name").keyup(function () {
    let search_reg = $("#boat-reg").val();
    let search_phone = $("#phone-number").val();
    let search_name = $("#boat-name").val();
    if (search_reg !== "" || search_phone !== "" || search_name !== "") {
        $.ajax({
            url: "/search",
            type: "POST",
            data: JSON.stringify({ 
                boat_reg: search_reg, 
                phone_number: search_phone, 
                boat_name: search_name 
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                console.log(data);
                let new_html = "";
                $.each(data, function (key, value) {
                    new_html += "<tr>";
                    new_html += "<td>" + value['boat_reg'] + "</td>";
                    new_html += "<td>" + value['phone_number'] + "</td>";
                    new_html += "<td>" + value['boat_name'] + "</td>";
                    new_html += "<td>" + value['visits'].length + "</td>";
                    new_html += "</tr>";
                });
                $("#search-results tbody").html(new_html);
            },
        });
    } else {
        $("#search-results tbody").html("");
    }
});
