import gradio as gr
import pandas as pd
from utils import load_models
from engine.discussion_engine import DiscussionEngine

llm_model, llm_tok, vlm_model, vlm_tok = load_models()

def start_discussion(image, question):
    engine = DiscussionEngine(
        image, question,
        llm_model, llm_tok,
        vlm_model, vlm_tok
    )
    team_df = pd.DataFrame(engine.team)
    return engine, engine.report, engine.diff, team_df, 1, ""

def next_round_step(engine, round_num, prev_fb):
    result = engine.run()

    return engine, round_num+1, prev_fb, {}, {}, "", {}, "", result, ""

with gr.Blocks() as demo:
    gr.Markdown("## Multi-Agent Medical QA")
    with gr.Column():
        img_in  = gr.Image(type="pil")
        q_in    = gr.Textbox()
        btn1    = gr.Button("Start")
        report  = gr.Textbox()
        diff    = gr.Textbox()
        team    = gr.Dataframe()
    with gr.Column():
        out     = gr.Textbox()

    btn1.click(fn=start_discussion,
               inputs=[img_in, q_in],
               outputs=[gr.State(), report, diff, team, gr.State(), gr.State()])
    demo.launch()
