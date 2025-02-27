# Use the official PostgreSQL 15 image
FROM postgres:15

# Install necessary packages including git and pgvector extension
RUN apt-get update && apt-get install -y \
      postgresql-server-dev-15 \
      gcc \
      make \
      git && \
    git clone https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && make install && \
    cd .. && rm -rf pgvector && \
    apt-get remove -y gcc make postgresql-server-dev-15 && \
    apt-get autoremove -y && \
    apt-get clean

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=rag_qna_db

# Expose the PostgreSQL port
EXPOSE 5432