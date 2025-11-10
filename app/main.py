# -*- coding: utf-8 -*-
"""
@File    : main.py
@Time    : 2025/10/31 15:14
@Desc    : 
"""
from fastapi import FastAPI
from app.api import routes_town

app = FastAPI(title="NeuroTown 心川镇")

app.include_router(routes_town.router, prefix="/town", tags=["Town"])


@app.get("/")
async def root():
    return {'message': "欢迎来到心川镇"}
