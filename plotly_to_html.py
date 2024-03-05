from data_processing import schoolDistribution, add_new_project, genderVsFinal, schoolSupportVsFamilySupport, weekdayAlcoholVsWeekendAlcohol
from app import app


def render_genderVsFinal():
    fig = genderVsFinal()
    graph_html = fig.to_html(full_html=False)
    return graph_html
    

def render_schoolDistribution():
    fig = schoolDistribution()
    graph_html = fig.to_html(full_html=False)
    return graph_html