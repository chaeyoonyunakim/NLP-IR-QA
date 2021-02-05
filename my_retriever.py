#\title{Document Retrieval}
#\author{Chaeyoon.Kim@city.ac.uk}
#\date{5 Feb 2021}

import math
class Retrieve:
    # Create new Retrieve object storing index, termWeighting scheme, and new create_dictionary 
    def __init__(self, index, termWeighting):    
        self.index = index
        self.termWeighting = termWeighting
        self.doc_dict, self.distance_dict = self.create_dict()        
     
    # doc_dict is a two-level dictionary mapping {doc_id->{term->counts}}.
    # distance_dict is a dictionary mapping {doc_id -> distance} to compute similarity scores in later coding forQuery.
    def binary_doc_dict(self, doc_dict, distance_dict):
        for term in self.index:
            sub_dict = self.index[term]
            for doc_id in sub_dict:
                if doc_id not in doc_dict:
                    doc_dict[doc_id] = {}
                    distance_dict[doc_id] = 0
                    doc_dict[doc_id][term] = 1 #'binary' is to justify the presence of term as 0 or 1, so it doesn't have to increase its count.
                    distance_dict[doc_id] += 1**2 #because of binary count, distance is also sum of ones or zeroes.
                else:
                    doc_dict[doc_id][term] = 1 #if the term have already existed in the dictionary, count 1 as same as done for first presence.
                    distance_dict[doc_id] += 1**2
        return doc_dict, distance_dict   
    def tf_doc_dict(self, doc_dict, distance_dict):
        for term in self.index:
            sub_dict = self.index[term]
            for doc_id in sub_dict:
                if doc_id not in doc_dict:
                    doc_dict[doc_id] = {}
                    distance_dict[doc_id] = 0
                    doc_dict[doc_id][term] = sub_dict[doc_id] #'tf' is working to define term frequency.
                    distance_dict[doc_id] += sub_dict[doc_id]**2 #sum of squared values to compute the size of each doc vector in later.
                else:
                    doc_dict[doc_id][term] = sub_dict[doc_id]
                    distance_dict[doc_id] += sub_dict[doc_id]**2
        return doc_dict, distance_dict         
    def tfidf_doc_dict(self, doc_dict, distance_dict):
        # collect all documents in corpus
        for term, docs in self.index.items():
            for doc_id, counts in docs.items():
                if doc_id not in doc_dict:
                    doc_dict[doc_id] = {}
                    doc_dict[doc_id][term] = counts
                else:
                    doc_dict[doc_id][term] = counts
        # number of documents in corpus            
        no_docs = len(doc_dict)
        # compute tf.idf and allocate it in doc_dict
        for term in self.index:
            sub_dict = self.index[term]
            for doc_id in sub_dict: #it needs to call the data stored in doc_dict but also needs to initialise dictionary for doc_id
                if doc_id not in distance_dict: #use distance_dict as an empty initial dictionary
                    distance_dict[doc_id] = 0
                    term_idf = math.log(no_docs/ len(sub_dict))
                    doc_dict[doc_id][term] *= term_idf
                    distance_dict[doc_id] += doc_dict[doc_id][term]**2
                else:
                    term_idf = math.log(no_docs/ len(sub_dict))
                    doc_dict[doc_id][term] *= term_idf #tf*idf
                    distance_dict[doc_id] += doc_dict[doc_id][term]**2
        return doc_dict, distance_dict

    def create_dict(self): #take the dictionaries from above return results to use them forQuery
        doc_dict = {}
        distance_dict = {}
        if self.termWeighting == 'binary':
            doc_dict, distance_dict = self.binary_doc_dict(doc_dict, distance_dict)
        elif self.termWeighting == 'tf':
            doc_dict, distance_dict = self.tf_doc_dict(doc_dict, distance_dict)
        elif self.termWeighting == 'tfidf':
            doc_dict, distance_dict = self.tfidf_doc_dict(doc_dict, distance_dict)            
        else:
            pass            
        return doc_dict, distance_dict #the union of the document sets
    
    # Method performing retrieval for specified query.
    # the candidate set is a dictionary mapping query-terms to counts.
    def forQuery(self, queries):
        binary = "binary"
        tf= "tf"
        tfidf = "tfidf"
        
        #implement binary
        if self.termWeighting == binary:        
            similarity_score = {}
            for doc_id in self.doc_dict:
                similarity_score[doc_id] = 0
                for term in queries:
                    if term in self.doc_dict[doc_id]:
                        similarity_score[doc_id] += 1
                similarity_score[doc_id] /= (self.distance_dict[doc_id]**(1/2)) #divided into the size of each doc vector.
            output = sorted(similarity_score, key=lambda x:similarity_score[x], reverse=True) #sort in descending order.
            return output #Top 10 will be retrieved because ir_engine.py stores the first 10 elements[:10] from this output (Retrieval Results).
        
        #implement tf
        elif self.termWeighting == tf:
            similarity_score = {}
            for doc_id in self.doc_dict:
                similarity_score[doc_id] = 0
                for term in queries:
                    if term in self.doc_dict[doc_id]: #if yes -> dot -> sum.
                        similarity_score[doc_id] += self.doc_dict[doc_id][term]*queries[term] #sum of multiplied values with a document and a query.
                similarity_score[doc_id] /= (self.distance_dict[doc_id]**(1/2))
            output = sorted(similarity_score, key=lambda x:similarity_score[x], reverse=True) #sort in descending order.
            return output
        
        #implement tfidf
        elif self.termWeighting == tfidf:
            no_docs = len(self.doc_dict) #number of documents in corpus
            similarity_score = {}
            term_computed = {}
            for doc_id in self.doc_dict:
                similarity_score[doc_id] = 0
                for term in queries:
                    if term in self.doc_dict[doc_id]: #if yes -> dot -> sum.
                        if term not in term_computed:
                            term_computed[term] = True
                            term_idf = math.log(no_docs/len(self.index[term]))
                            queries[term] *= term_idf #tf*idf
                        similarity_score[doc_id] += self.doc_dict[doc_id][term]*queries[term] #sum of multiplied values with a document and a query.
                similarity_score[doc_id] /= (self.distance_dict[doc_id]**(1/2))
            output = sorted(similarity_score, key=lambda x:similarity_score[x], reverse=True) #sort in descending order.
            return output
           
        else:
            print("Check the termWeighting")
            return range(1,11)