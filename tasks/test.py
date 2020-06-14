from invoke import task


@task(default=True)
def run(ctx):
    """Run test cases"""
    ctx.run(f"pytest", pty=True)


@task
def cov(ctx):
    """Run test covreage check"""
    ctx.run(f"pytest --cov=report_generator tests/", pty=True)
