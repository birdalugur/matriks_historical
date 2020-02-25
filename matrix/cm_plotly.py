### Confusion Matrix'i plotly kullanarak çizdirmek için >>>>>
import plotly.graph_objects as go


def __get_layout(x_name: str, y_name: str):
    layout = {
        "title": "Confusion Matrix",
        "xaxis": {
            "title": x_name,
            "titlefont": {
                "size": 18,
                "color": "#7f7f7f",
                "family": "Courier New, monospace"
            }
        },
        "yaxis": {
            "title": y_name,
            "titlefont": {
                "size": 18,
                "color": "#7f7f7f",
                "family": "Courier New, monospace"
            }
        },
        "barmode": "overlay"
    }

    return layout


def draw_matrix(c_matrix: np.ndarray, x_name: str, y_name: str) -> go.Figure:
    trace1 = {
        "type": "heatmap",
        "x": ["up", "down"],
        "y": ["up", "const", "down"],
        "z": c_matrix,
        "colorscale": "Blues"
    }
    data = go.Data([trace1])
    layout = __get_layout(x_name, y_name)
    fig = go.Figure(data=data, layout=layout)
    return fig
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
