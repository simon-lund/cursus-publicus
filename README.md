# [Cursus Publicus](https://de.wikipedia.org/wiki/Cursus_publicus)
This is a simple proof of concept for a stand-alone [ReST](https://de.wikipedia.org/wiki/Representational_State_Transfer) event hub inspired by this blog post [Give me /events, not webhooks](https://blog.syncinc.so/events-not-webhooks?utm_source=hackernewsletter&utm_medium=email&utm_term=code).

## 🛠️ Technologies
- (Redis)[https://redis.io/]
- (FastAPI)[https://fastapi.tiangolo.com/]

## ⏳ Installation
After installing Redis run `uvicorn main:app --reload` to start the app. 
Once running check out the docs at http://127.0.0.1:8000/docs.

## 💤 Backlog
- [ ] Long-polling
- [ ] Event pagination
- [ ] Manage & Monitoring APIs (delete events, search for events, reset)
- [ ] Global events
- [ ] .env
