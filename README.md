This is my basic template for creating an airflow instance with docker.

Check out the blog post [here](https://dabble-of-devops.com/learn-airflow-by-example-part-1-introduction/).

Bring the template up with:

```
docker-compose up -d
```

The first time it will take a minute to initialize. Then check out the webserver at `localhost:8089`.

To see more docker-compose helper commands check out the `bring_up_airflow_stack.sh`.
