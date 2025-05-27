const marginTop = 40;
const marginRight = 30;
const marginBottom = 0;
const marginLeft = 100;
const barStep = 40;
const barPadding = 10 / barStep;
const duration = 750;
const width = 960;

const color = d3.scaleOrdinal([true, false], ["steelblue", "#aaa"]);

const x = d3.scaleLinear().range([marginLeft, width - marginRight]);

const xAxis = g => g
    .attr("class", "x-axis")
    .attr("transform", `translate(0,${marginTop})`)
    .call(d3.axisTop(x).ticks(width / 80, "s"))
    .call(g => (g.selection ? g.selection() : g).select(".domain").remove());

const yAxis = g => g
    .attr("class", "y-axis")
    .attr("transform", `translate(${marginLeft + 0.5},0)`)
    .call(g => g.append("line")
        .attr("stroke", "currentColor")
        .attr("y1", marginTop)
        .attr("y2", height - marginBottom));

const tooltip = d3.select("#hierarchical_chart_tooltip");

let root;
let height;

function hierarchical_chart() {
    const svg = d3.select("#hierarchical_chart").append("svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("width", width)
        .attr("height", height)
        .attr("style", "max-width: 100%; height: auto;");

    x.domain([0, root.value]);

    svg.append("rect")
        .attr("class", "background")
        .attr("fill", "none")
        .attr("pointer-events", "all")
        .attr("width", width)
        .attr("height", height)
        .attr("cursor", "pointer")
        .on("click", (event, d) => up(svg, d));

    svg.append("g").call(xAxis);
    svg.append("g").call(yAxis);

    down(svg, root);
}


function bar(svg, down, d, selector) {
    const g = svg.insert("g", selector)
        .attr("class", "enter")
        .attr("transform", `translate(0,${marginTop + barStep * barPadding})`)
        .attr("text-anchor", "end")
        .style("font", "13px sans-serif");

    const bar = g.selectAll("g")
        .data(d.children)
        .join("g")
        .attr("cursor", d => !d.children ? null : "pointer")
        .on("click", (event, d) => down(svg, d));

    bar.append("text")
        .attr("x", marginLeft - 6)
        .attr("y", barStep * (1 - barPadding) / 2)
        .attr("dy", ".35em")
        .text(d => d.data.name);

    bar.append("rect")
        .attr("x", x(0))
        .attr("width", d => x(d.value) - x(0))
        .attr("height", barStep * (1 - barPadding))
        .attr("fill", d => color(!!d.children))
        .on("mouseover", function (event, d) {
            tooltip.style("visibility", "visible")
                .text(`${d.data.name}: ${d.value}`);
            d3.select(this).attr("stroke", "black").attr("stroke-width", 1.5);
        })
        .on("mousemove", function (event) {
            tooltip
                .style("top", (event.pageY - 10) + "px")
                .style("left", (event.pageX + 10) + "px");
        })
        .on("mouseout", function () {
            tooltip.style("visibility", "hidden");
            d3.select(this).attr("stroke", null);
        });

    return g;
}

function down(svg, d) {
    // Check if there are children to drill down to
    if (!d.children) return;

    // Check for active transitions (approach compatible with D3.js v7)
    if (svg.classed("transition-active")) return;
    svg.classed("transition-active", true);

    svg.select(".background").datum(d);

    const transition1 = svg.transition().duration(duration);
    const transition2 = transition1.transition();

    const exit = svg.selectAll(".enter").attr("class", "exit");

    exit.selectAll("rect")
        .attr("fill-opacity", p => p === d ? 0 : null)

    exit.transition(transition1).attr("fill-opacity", 0).remove();

    const enter = bar(svg, down, d, ".y-axis").attr("fill-opacity", 0);

    enter.transition(transition1).attr("fill-opacity", 1);

    enter.selectAll("g")
        .attr("transform", stack(d.index))
        .transition(transition1)
        .attr("transform", stagger())

    x.domain([0, d3.max(d.children, d => d.value)]);
    svg.selectAll(".x-axis").transition(transition2).call(xAxis);

    enter.selectAll("g").transition(transition2)
        .attr("transform", (d, i) => `translate(0,${barStep * i})`); enter.selectAll("rect")
            .attr("fill", color(true))
            .transition(transition2)
            .attr("fill", d => color(!!d.children))
            .attr("width", d => x(d.value) - x(0))
            .on("end", () => svg.classed("transition-active", false));
}

function up(svg, d) {
    // Check if we can go up a level and no active transitions
    if (!d.parent || !svg.selectAll(".exit").empty() || svg.classed("transition-active")) return;
    svg.classed("transition-active", true);

    svg.select(".background").datum(d.parent);

    const transition1 = svg.transition().duration(duration);
    const transition2 = transition1.transition();

    const exit = svg.selectAll(".enter").attr("class", "exit");

    x.domain([0, d3.max(d.parent.children, d => d.value)]);
    svg.selectAll(".x-axis").transition(transition1).call(xAxis);

    exit.selectAll("g").transition(transition1).attr("transform", stagger());
    exit.selectAll("g").transition(transition2).attr("transform", stack(d.index));
    exit.selectAll("rect").transition(transition1)
        .attr("width", d => x(d.value) - x(0))
        .attr("fill", color(true));
    exit.transition(transition2).attr("fill-opacity", 0).remove();

    const enter = bar(svg, down, d.parent, ".exit").attr("fill-opacity", 0);
    enter.selectAll("g")
        .attr("transform", (d, i) => `translate(0,${barStep * i})`);
    enter.transition(transition2).attr("fill-opacity", 1); enter.selectAll("rect")
        .attr("fill", d => color(!!d.children))
        .attr("fill-opacity", p => p === d ? 0 : null)
        .transition(transition2)
        .attr("width", d => x(d.value) - x(0))
        .on("end", function (p) {
            d3.select(this).attr("fill-opacity", 1);
            svg.classed("transition-active", false);
        });
}

function stack(i) {
    let value = 0;
    return d => {
        // Ensure i is a valid number to prevent NaN in translate
        if (i === undefined || isNaN(i)) {
            i = 0;
        }
        // Ensure value is a valid number
        if (isNaN(value) || value === undefined) {
            value = 0;
        }
        const offsetX = x(value) - x(0);
        const offsetY = barStep * i;
        const t = `translate(${offsetX},${offsetY})`;

        // Only add the value if it's a valid number
        if (d && !isNaN(d.value)) {
            value += d.value;
        }
        return t;
    };
}

function stagger() {
    return (d, i) => {
        // Ensure i is a valid number
        if (i === undefined || isNaN(i)) {
            i = 0;
        }
        return `translate(0,${barStep * i})`;
    };
}