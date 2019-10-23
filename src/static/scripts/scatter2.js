const ACC = 800;
const split = 800;

function linspace(start, stop, step) {
    let ret = [];
    let i = start;
    while (Math.round(i * ACC) <= Math.round(stop * ACC)) {
        ret.push(i);
        i += step;
    }
    // console.log(Math.round(i * ACC), Math.round(stop * ACC));
    return ret;
}

function contour_trace(x, y, z, axis) {
    return {
        x: x,
        y: y,
        z: z,
        connectgaps: true,
        // opacity: 0.9,
        type: 'contour',
        line:{
            smoothing: 0.7
        },
        // zsmooth: 'fast',
        xaxis: 'x' + axis,
        yaxis: 'y' + axis,
        colorscale: [
            ['0.0', '#8A0002'], ['0.05', '#A50026'], ['0.15', '#DC3A2B'], ['0.25', '#F67E4B'],
            ['0.35', '#FDC272'], ['0.45', '#FEEFA5'], ['0.55', '#E3F399'], ['0.65', '#B1DD71'],
            ['0.75', '#6DC063'], ['0.85', '#219B51'], ['0.95', '#006837'], ['1.0', '#085a2e']
        ],
        contours: {
            // coloring: 'heatmap',
        },
        hoverinfo: 'skip'
    };
}

function point_trace(x, y, text, axis, color) {
    return {
        x: x,
        y: y,
        text: text,
        mode: 'markers',
        hoverinfo: 'text',
        type: 'scattergl',
        name: 'text',
        opacity: 0.9,
        xaxis: 'x' + axis,
        yaxis: 'y' + axis,
        marker: {
            sizemin: 30,
            sizemax: 30,
            size: 5,
            line: {
                width: 0.4,
                color: '#777777'
            },
            color: color
        },
        showlegend: false
    };
}

let colorList = ['#A50026', '#DC3A2B', '#F67E4B', '#FDC272', '#FEEFA5', '#E3F399', '#B1DD71', '#6DC063', '#219B51', '#006837'];
let scatter_data = [];
let point_xValues = [];
let point_yValues = [];
let point_labels = [];
let point_preds = [];
let point_color_label = [];
let point_color_pred = [];
let contour_xValues = [];
let contour_yValues = [];
let contour_labels = [];
let contour_preds = [];
let z_n_labels = [];
let z_n_preds = [];

let x_max = Number.MIN_VALUE;
let x_min = Number.MAX_VALUE;
let y_max = Number.MIN_VALUE;
let y_min = Number.MAX_VALUE;

let x_start = 0;
let x_end = 0;
let y_start = 0;
let y_end = 0;

const config = {
    scrollZoom: true
};

let layout2 = {
    title: '',
    dragmode: "pan",
    hovermode: "closest",
    xaxis: {
        domain: [0, 0.49],
        // anchor: 'y1',
        ticks: '',
        showticklabels: false,
        autorange: true
    },
    yaxis: {
        domain: [0, 1],
        // anchor: 'x1'
        ticks: '',
        showticklabels: false,
        autorange: true
    },
    xaxis2: {
        domain: [0.51, 1],
        matches: 'x',
        // anchor: 'y2',
        ticks: '',
        showticklabels: false,
        autorange: true
    },
    yaxis2: {
        domain: [0, 1],
        matches: 'y',
        // anchor: 'x1',
        ticks: '',
        showticklabels: false,
        autorange: true
    },
    // grid: {rows: 1, columns: 2, pattern: 'independent'},
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    margin: {
        l: 20,
        r: 20,
        b: 20,
        t: 20,
        // pad: 50
    }
};

d3.csv('/static/data/sent_plot.csv').then(function (data) {
    data.forEach(function (d) {
        point_xValues.push(parseFloat(d.x));
        point_yValues.push(parseFloat(d.y));
        point_labels.push(d.label);
        point_preds.push(d.pred);
        point_color_label.push(colorList[parseInt(d.label) - 1]);
        point_color_pred.push(colorList[parseInt(d.pred) - 1]);
        x_max = Math.max(x_max, d.x);
        x_min = Math.min(x_min, d.x);
        y_max = Math.max(y_max, d.y);
        y_min = Math.min(y_min, d.y);
    });
    x_start = Math.round(x_min * ACC) / ACC;
    x_end = Math.round(x_max * ACC) / ACC;
    contour_xValues = linspace(x_start, x_end, 1 / split);

    y_start = Math.round(y_min * ACC) / ACC;
    y_end = Math.round(y_max * ACC) / ACC;
    contour_yValues = linspace(y_start, y_end, 1 / split);

    // console.log(x_start, x_end, y_start, y_end);
    // console.log(contour_xValues, contour_yValues);

    let x_length = contour_xValues.length;
    let y_length = contour_yValues.length;

    contour_labels = new Array(y_length);
    z_n_labels = new Array(y_length);
    contour_preds = new Array(y_length);
    z_n_preds = new Array(y_length);
    for (let i = 0; i < y_length; i++) {
        contour_labels[i] = new Array(x_length);
        z_n_labels[i] = new Array(x_length);
        contour_preds[i] = new Array(x_length);
        z_n_preds[i] = new Array(x_length);
        for (let j = 0; j < x_length; j++) {
            contour_labels[i][j] = null;
            z_n_labels[i][j] = 0;
            contour_preds[i][j] = null;
            z_n_preds[i][j] = 0;
        }
    }
    data.forEach(function (d) {
        x_coor = Math.round((parseFloat(d.x) - x_start) * split);
        y_coor = Math.round((parseFloat(d.y) - y_start) * split);
        if (contour_labels[y_coor][x_coor] != null) {
            contour_labels[y_coor][x_coor] = parseInt(d.label);
            z_n_labels[y_coor][x_coor]++;
        } else {
            contour_labels[y_coor][x_coor] = (contour_labels[y_coor][x_coor] * z_n_labels[y_coor][x_coor] + parseInt(d.label)) / (z_n_labels[y_coor][x_coor] + 1);
            z_n_labels[y_coor][x_coor]++;
        }
        if (contour_preds[y_coor][x_coor] != null) {
            contour_preds[y_coor][x_coor] = parseInt(d.pred);
            z_n_preds[y_coor][x_coor]++;
        } else {
            contour_preds[y_coor][x_coor] = (contour_preds[y_coor][x_coor] * z_n_preds[y_coor][x_coor] + parseInt(d.pred)) / (z_n_preds[y_coor][x_coor] + 1);
            z_n_preds[y_coor][x_coor]++;
        }
    });
}).then(function () {
    scatter_data.push(contour_trace(contour_xValues, contour_yValues, contour_preds, ''));
    scatter_data.push(point_trace(point_xValues, point_yValues, point_preds, '', point_color_pred));
    // scatter_data.push(contour_trace(contour_xValues, contour_yValues, contour_labels, '2'));
    scatter_data.push(point_trace(point_xValues, point_yValues, point_labels, '2', point_color_label));

    Plotly.newPlot('scatter', scatter_data, layout2, config);

    let myPlot = document.getElementById('scatter');

    myPlot.on('plotly_hover', function(eventdata) {
        // let points = eventdata.points[0], pointNum = points.pointNumber;
        let hover_x = eventdata.xvals[0], hover_y = eventdata.yvals[0];
        // console.log(pointNum);
        Plotly.Fx.hover('scatter',
            [
                {curveNumber: 1, xval: hover_x, yval: hover_y},
                {curveNumber: 2, xval: hover_x, yval: hover_y}
            ],
            ['xy', 'x2y2']
        );
    });
});