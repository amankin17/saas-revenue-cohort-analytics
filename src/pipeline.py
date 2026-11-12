"""Synthetic SaaS subscriptions and reproducible SQLite metrics."""
import sqlite3, random
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]

def plus_month(month,offset):
    y,m=map(int,month.split('-'))
    n=y*12+(m-1)+offset
    return f'{n//12:04d}-{n%12+1:02d}'

def make_data(n=250,seed=42):
    rng=random.Random(seed)
    result=[]
    for customer in range(1,n+1):
        signup=plus_month('2026-01',rng.randrange(6))
        tenure=rng.choice([None,None,None,1,2,3,4,5])
        cancel=plus_month(signup,tenure) if tenure is not None else None
        fee=rng.choice([29,49,99,199])
        result.append((customer,signup,cancel,fee))
    return result

def database(rows):
    connection=sqlite3.connect(':memory:')
    connection.execute('CREATE TABLE subscriptions(customer_id INTEGER PRIMARY KEY, start_month TEXT NOT NULL, end_month TEXT, monthly_fee REAL NOT NULL)')
    connection.executemany('INSERT INTO subscriptions VALUES(?,?,?,?)',rows)
    return connection

def kpi(conn,month):
    sql=(BASE/'sql/kpis.sql').read_text()
    _, active, mrr=conn.execute(sql,{'month':month}).fetchone()
    previous=plus_month(month,-1)
    prev_active=conn.execute('SELECT COUNT(*) FROM subscriptions WHERE start_month<=? AND (end_month IS NULL OR end_month>?)',(previous,previous)).fetchone()[0]
    lost=conn.execute('SELECT COUNT(*) FROM subscriptions WHERE end_month=?',(month,)).fetchone()[0]
    churn=round(lost/prev_active,4) if prev_active else None
    return {'month':month,'active_accounts':active,'mrr':mrr,'logo_churn':churn}

def cohorts(conn,month):
    sql=(BASE/'sql/cohorts.sql').read_text()
    return [{'cohort':c,'size':n,'active':a,'retention':round(a/n,3)} for c,n,a in conn.execute(sql,{'month':month})]

if __name__=='__main__':
    import json
    conn=database(make_data())
    for month in ['2026-04','2026-05','2026-06']:
        print(json.dumps(kpi(conn,month)))
    print('Cohorts (June 2026):',json.dumps(cohorts(conn,'2026-06'),indent=2))
