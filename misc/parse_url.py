import random
import urlparse

from misc.utils import id_generator


def fuzz_url_path(url):
    r = urlparse.urlparse(url)
    if len(r.query) == 0:
        url_path = r.path
        path_elem = str(url_path).split('/')
        # print "path_elem:" + str(path_elem)
        select_elem = random.choice(path_elem)
        # print "select elem:" + str(select_elem)

        # fuzz selected element
        for i, item in enumerate(path_elem):
            # print "i:" + str(i)
            # print "item:" + str(item)
            if item == select_elem:
                if i == 0:
                    pass
                else:
                    path_elem[i] = id_generator(random.randint(1,64))
                    # print "i:" + str(i)
                    # print "path_elem[i]:" + str(path_elem[i])

        new_path = '/'.join(path_elem)
        # print "new_path:" + str(new_path)
        new_url = r.scheme + "://" + r.netloc + new_path
    else:
        url_path = r.path + "?" + r.query
        if "&" in r.query:
            path_query_params_con = r.query.split("&")
            # print "path_query_params_con1:" + str(path_query_params_con)
            for items in path_query_params_con:
                if "=" in items: 
                    path_query_params_equal = items.split("=")
                    # print "path_query_params_split" + str(path_query_params_equal)
                    select_path_query_params = random.choice(path_query_params_equal)
                    # print "aaaaa:" + str(select_path_query_params)
                    # fuzz selected element
                    index_random = path_query_params_equal.index(select_path_query_params)
                    # print "index_random:" + str(index_random)
                    path_query_params_equal[index_random] = id_generator(random.randint(1,64))
                    # print "new list:" + str(path_query_params_equal)
                    new_query_path_equal = '='.join(path_query_params_equal)
                    # print "new path:" + str(new_query_path_equal)
                    path_query_params_con[path_query_params_con.index(items)] = new_query_path_equal
                    # print "new full list:" + str(path_query_params_con)
                    # path_query_params_con.append(new_query_path_equal)
            new_query_path = "&".join(path_query_params_con)
            # print "new_query_path:" + str(new_query_path)
        
        path_elem = str(url_path).split('/')
        # print "path_elem:" + str(path_elem)
        select_elem = random.choice(path_elem)
        # print "select elem:" + str(select_elem)

        # fuzz selected element
        for i, item in enumerate(path_elem):
            # print "i:" + str(i)
            # print "item:" + str(item)
            if item == select_elem:
                if i == 0:
                    pass
                else:
                    path_elem[i] = id_generator(random.randint(1,64))
                    # print "i:" + str(i)
                    # print "path_elem[i]:" + str(path_elem[i])
            # new_url = r.scheme + "://" + r.netloc + new_path

        new_path = '/'.join(path_elem[:-1])
        # del new_path[-1]
        # print "new_path:" + str(new_path)
        new_url = r.scheme + "://" + r.netloc + new_path + "/search_contract?" + new_query_path
        print "new url:" + str(new_url)

    return new_url


if __name__ == '__main__':
    test_url = "http://10.187.3.58:8774/v2/9ac08939bf67465c88cd638107e0a6d6/os-tag-types/11/extra-specs"
    for i in range(100):
        print fuzz_url_path(test_url)
