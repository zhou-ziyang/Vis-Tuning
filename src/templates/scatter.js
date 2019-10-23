function plot_scatter(file, target, source) {
    let classes = 10;

    let colorList = ['#A50026','#DC3A2B','#F67E4B','#FDC272','#FEEFA5','#E3F399','#B1DD71','#6DC063','#219B51','#006837'];
    // let colorList = ['#C23843', '#C24C43', '#C25E43', '#C26D43', '#C27543', '#C28743', '#C29343', '#C2A943', '#C2C543', '#C2D443'];
    let map = [0, 9, 2, 7, 3, 6, 1, 8, 4, 5];
    let scatter_data = new Array(classes);
    let colors = [];

    for (let i  = 0; i < classes; i++) {
        scatter_data[i] = {
            x: [],
            y: [],
            text: [],
            mode: 'markers',
            hoverinfo: 'text',
            type: 'scattergl',
            name: (map[i] + 1).toString() + " stars",
            opacity: 0.9,
            marker: {
                sizemin: 20,
                sizemax: 20,
                // size: 5,
                color: colorList[map[i]]
            }
        };
    }



    let layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        xaxis: {
            // range: [-0.03, 0.03],
            // autorange: true
            showspikes: false
        },
        yaxis: {
            // range: [-0.02, 0.02],
            // autorange: true
            showspikes: false
        },
        title:'',
        dragmode: "pan",
        hovermode: "closest",
        displayModeBar: false
    };

    let config = {
        displayModeBar: false,
        scrollZoom: true
    };

    d3.csv(file).then(function (data) {
        data.forEach(function (d) {
            pred = d.pred;
            label = d.label;
            let target = scatter_data[map.indexOf(parseInt(window[source]) - 1)];
            target.x.push(parseFloat(d.x));
            target.y.push(parseFloat(d.y));
            target.text.push(window[source]);
        });
    }).then(function () {
        Plotly.newPlot(target, scatter_data, layout, config);
    });
}

plot_scatter('sent_plot.csv', 'scatter_pred', 'pred');
plot_scatter('sent_plot.csv', 'scatter_label', 'label');