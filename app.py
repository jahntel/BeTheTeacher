from __future__ import annotations
import json
import streamlit as st
from mwangaza import store

st.set_page_config(page_title='Mwangaza AI', page_icon='🌱', layout='wide')
store.init_db()
if not store.list_learners(): store.seed_demo()

st.title('🌱 Mwangaza AI')
st.caption('Every learner has a story. Make the patterns visible. · Teacher-facing prototype · Synthetic data only')
with st.sidebar:
    st.header('Teacher workspace')
    st.warning('Demo mode: use synthetic records only. This is not a production student information system.')
    learners=store.list_learners()
    learner_ids=[x['learner_id'] for x in learners]
    selected=st.selectbox('Select learner',learner_ids,format_func=lambda x: next((f"{x} — {y['display_name']} ({y['grade']})" for y in learners if y['learner_id']==x),x))
    if st.button('Build / refresh draft profile', type='primary', use_container_width=True):
        try:
            profile=store.build_profile(selected,actor='demo-teacher')
            st.success(f"Draft profile {profile['profile_id']} created.")
        except Exception as e: st.error(str(e))
    st.divider()
    st.markdown('**Quick actions**')
    if st.button('Seed synthetic records',use_container_width=True):
        store.seed_demo(); st.rerun()

learner=next((x for x in learners if x['learner_id']==selected),None)
evidence=store.list_evidence(selected)
profiles=store.list_profiles(selected)
reviews=store.list_reviews('pending')
reviews=[r for r in reviews if r['learner_id']==selected]
col1,col2,col3,col4=st.columns(4)
col1.metric('Evidence records',len(evidence))
col2.metric('Recorded terms',len(set(x['term'] for x in evidence)))
col3.metric('Draft profiles',len(profiles))
col4.metric('Pending reviews',len(reviews))

profile_tab,timeline_tab,add_tab,review_tab,audit_tab=st.tabs(['Learner profile','Evidence timeline','Add evidence','Teacher review','Audit log'])
with profile_tab:
    st.subheader('Longitudinal profile')
    if not profiles:
        st.info('No profile has been generated yet. Select “Build / refresh draft profile” to create one from the evidence shown in the timeline.')
    else:
        p=profiles[0]
        st.caption(f"Profile {p['profile_id']} · Version {p['version']} · {p['status'].upper()} · {p['created_at']}")
        st.info(p['summary'])
        st.markdown('#### Potential patterns — teacher interpretation required')
        ev_by_id={x['evidence_id']:x for x in evidence}
        for pattern in p['patterns']:
            with st.container(border=True):
                st.markdown(f"**{pattern['type'].replace('_',' ').title()} · {pattern['subject']}**")
                st.write(pattern['statement'])
                st.caption('Evidence: '+', '.join(pattern['evidence_ids']))
                with st.expander('Inspect source evidence'):
                    for eid in pattern['evidence_ids']:
                        x=ev_by_id.get(eid)
                        if x: st.write(f"**{eid} — {x['title']}** · {x['term']} · {x['subject']} · {x['score']}/{x['max_score']}" if x['score'] is not None else f"**{eid} — {x['title']}** · {x['term']} · {x['subject']}")
                        if x: st.caption(f"Source: {x['source_ref']} · {x['observation']}")
                if st.button('Flag for teacher review',key='flag_'+p['profile_id']+'_'+pattern['type']+'_'+pattern['subject']):
                    try:
                        store.flag_review(selected,pattern['statement'],f"Review the evidence and consider context for {pattern['subject']}.",pattern['evidence_ids'],actor='demo-teacher')
                        st.success('Review task created; no sharing occurred.')
                    except Exception as e: st.error(str(e))
        st.warning('This profile is descriptive, provisional, and not a diagnosis or pathway recommendation.')
with timeline_tab:
    st.subheader('Evidence timeline')
    if evidence:
        st.dataframe([{'Date':x['occurred_at'],'Term / Grade':x['term'],'Subject':x['subject'],'Type':x['evidence_type'],'Title':x['title'],'Score':f"{x['score']}/{x['max_score']}" if x['score'] is not None else '—','Evidence ID':x['evidence_id'],'Source':x['source_ref'],'Observation':x['observation']} for x in evidence],use_container_width=True,hide_index=True)
    else: st.info('No evidence yet.')
with add_tab:
    st.subheader('Add a new evidence record')
    with st.form('add_evidence_form'):
        date=st.date_input('Assessment / observation date')
        term=st.text_input('Term and grade',placeholder='Grade 6 · Term 2')
        subject=st.selectbox('Subject / area',['Mathematics','English','Kiswahili','Science','Social Studies','Attendance','Extracurricular','Other'])
        etype=st.selectbox('Evidence type',['quiz','assignment','project','teacher_observation','attendance','extracurricular'])
        title=st.text_input('Assessment / observation title')
        has_score=st.checkbox('This record has a numeric score')
        c1,c2=st.columns(2)
        score=c1.number_input('Score',min_value=0.0,value=0.0,step=1.0) if has_score else None
        maximum=c2.number_input('Maximum score',min_value=0.1,value=20.0,step=1.0) if has_score else None
        observation=st.text_area('What was observed? Avoid unsupported labels.')
        source_ref=st.text_input('Source reference',placeholder='e.g. Q-G6-T2-501')
        submitted=st.form_submit_button('Validate and save evidence')
        if submitted:
            try:
                result=store.add_evidence({'learner_id':selected,'occurred_at':date.isoformat(),'term':term,'subject':subject,'evidence_type':etype,'title':title,'score':score,'max_score':maximum,'observation':observation,'source_ref':source_ref},actor='demo-teacher')
                st.success(f"Saved {result['evidence_id']} and logged the action.")
                st.rerun()
            except Exception as e: st.error(str(e))
with review_tab:
    st.subheader('Human-in-the-loop review queue')
    st.caption('Only a named reviewer can decide. Approval records a decision; it does not automatically send information to a guardian.')
    all_reviews=[r for r in store.list_reviews() if r['learner_id']==selected]
    if not all_reviews: st.info('No review tasks for this learner.')
    for r in all_reviews:
        with st.container(border=True):
            st.markdown(f"**{r['task_id']} · {r['status'].upper()}**")
            st.write(r['pattern']); st.caption(r['rationale']); st.write('Evidence: '+', '.join(r['evidence_ids']))
            if r['status']=='pending':
                with st.form('decision_'+r['task_id']):
                    reviewer=st.text_input('Reviewer full name',key='name_'+r['task_id'])
                    note=st.text_area('Decision note / context',key='note_'+r['task_id'])
                    choice=st.radio('Decision',['approved','rejected'],horizontal=True,key='decision_'+r['task_id'])
                    if st.form_submit_button('Record human decision'):
                        try:
                            store.decide_review(r['task_id'],reviewer,choice,note)
                            st.success('Decision recorded in audit log.'); st.rerun()
                        except Exception as e: st.error(str(e))
            else: st.caption(f"Decision by {r['reviewer']} at {r['decided_at']}: {r['decision_note']}")
with audit_tab:
    st.subheader('Tool and action audit trail')
    st.caption('This prototype logs application actions and MCP tool outcomes. It is not tamper-proof or a replacement for production audit infrastructure.')
    logs=store.list_audit(200)
    st.dataframe([{'Timestamp':x['timestamp'],'Actor':x['actor'],'Action':x['action'],'Result':x['result'],'Inputs':x['input_json'],'Outputs':x['output_json']} for x in logs],use_container_width=True,hide_index=True)
    with st.expander('Raw audit JSON'):
        st.code(json.dumps(logs,indent=2,ensure_ascii=False),language='json')

st.divider()
st.caption('Mwangaza AI · Prototype only · No real learner data · Human judgment stays in control.')
