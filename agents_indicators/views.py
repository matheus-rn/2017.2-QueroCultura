from django.shortcuts import render
from .api_connection import RequestAgentsRawData


def build_temporal_indicator(data):
    temporal_indicator = {}

    for i in data:
        x = i["createTimestamp"]["date"].split("-")

        if not (x[0] in temporal_indicator):
            temporal_indicator[x[0]] = {}
            temporal_indicator[x[0]][x[1]] = 1
        elif not (x[1] in temporal_indicator.get(x[0])):
            temporal_indicator[x[0]][x[1]] = 1
        else:
            temporal_indicator[x[0]][x[1]] += 1

    return temporal_indicator
