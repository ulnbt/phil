# phil Guided Tour

Use this as a fast first-run walkthrough. Each step is copy/paste-ready.

## Controls

In REPL tutorial mode:

- `Enter` or `:next` moves to the next step
- `:repeat` shows the current step again
- `:done` exits tutorial mode

Start tutorial mode:

```bash
phil
```

```text
phil> :tutorial
```

Shortcut:

```text
phil> :t
```

## First-Minute Sequence

### Step 1: Forgiving Input + Calculus

```text
int(sinx)
```

Expected:

```text
-cos(x)
```

### Step 2: Exact Huge Integer Arithmetic

```text
10^10000 + 1 - 10^10000
```

Expected:

```text
1
```

### Step 3: Solve Equation

```text
solve(x^2 - 4 = 0, x)
```

Expected:

```text
[-2, 2]
```

### Step 4: Linear System Solve

```text
linalg solve A=[[2,1],[1,3]] b=[1,2]
```

Expected:

```text
Matrix([[1/5], [3/5]])
```

### Step 5: ODE Quick Win

```text
ode y' = y, y(0)=1
```

Expected:

```text
y(x) = exp(x)
```

### Step 6: Decimal Representation

```text
N(1/7, 20)
```

Expected:

```text
0.14285714285714285714
```

### Step 7: Recovery from a Mistake

Run this intentionally wrong:

```text
gcd(8)
```

You should see `E:` plus a `hint:`. Then fix it:

```text
gcd(8, 12)
```

Expected:

```text
4
```

## Next Commands

- Strict reference: `:h`
- Runnable patterns: `:examples`
- Progressive discovery: `?`, `??`, `???`
