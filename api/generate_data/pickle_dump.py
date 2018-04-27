# Needs to run in Alpha repo, with `make shell_plus` and the production database synced.
import pickle


def artist(press_source):
    talent = press_source.asset.talents.first()
    if not talent:
        return None
    return talent.display_name


prod = [[p.source_url, p.article_title, p.publication_date, p.sentiment, artist(p)]
        for p in PressSource.objects.all() if p.source_url]

with open('./prod.p', 'wb') as f:
    pickle.dump(prod, f)
